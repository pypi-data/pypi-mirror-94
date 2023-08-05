#include "PinkIndexer.h"

#include <algorithm>
#include <fstream>
#include <numeric>

#ifdef OPENMP_AVAILABLE
#include <omp.h>
#endif

using namespace std;
using namespace Eigen;

namespace pinkIndexer
{

    PinkIndexer::PinkIndexer(const ExperimentSettings& experimentSettings, ConsideredPeaksCount consideredPeaksCount, AngleResolution angleResolution,
                             RefinementType refinementType, float maxResolutionForIndexing_1_per_A)
        : reciprocalToRealProjection(experimentSettings)
        , backprojection(experimentSettings)
        , sinogram(experimentSettings.getSampleReciprocalLattice_1A())
        , refinement(experimentSettings.getTolerance())
        , sampleLattice(experimentSettings.getSampleReciprocalLattice_1A())
        , consideredPeaksCount(consideredPeaksCount)
        , angleResolution(angleResolution)
        , refinementType(refinementType)
        , maxResolutionForIndexing_1_per_A(maxResolutionForIndexing_1_per_A)
        , finalRefinementTolerance(experimentSettings.getTolerance())
    {
        float angleResolution_deg = getAngleResolution();
        sinogram.setSinogramAngleResolution(angleResolution_deg);
    }

    int PinkIndexer::indexPattern(Lattice& indexedLattice, Vector2f& centerShift, Array<bool, Dynamic, 1>& fittedPeaks, RowVectorXf& intensities,
                                  const Matrix3Xf& meanReciprocalPeaks_1_per_A, int threadCount)
    {
        if (meanReciprocalPeaks_1_per_A.cols() < 2)
            return 0;

        Matrix2Xf detectorPeaks_m;
        reciprocalToRealProjection.project(detectorPeaks_m, meanReciprocalPeaks_1_per_A);
        return indexPattern(indexedLattice, centerShift, fittedPeaks, intensities, detectorPeaks_m, threadCount);
    }

    int PinkIndexer::indexPattern(Lattice& indexedLattice, Vector2f& centerShift, Array<bool, Dynamic, 1>& fittedPeaks, RowVectorXf& intensities,
                                  const Matrix2Xf& detectorPeaks_m, int threadCount)
    {
        if (detectorPeaks_m.cols() < 2)
            return 0;

        Matrix3Xf ulsDirections; // Unit vector of ULS
        Array2Xf ulsBorderNorms; // 2 borders between intersection with the 2 Ewald spheres
        backprojection.backProject(detectorPeaks_m, ulsDirections, ulsBorderNorms);

        Matrix3Xf ulsDirections_reduced = ulsDirections;
        Array2Xf ulsBorderNorms_reduced = ulsBorderNorms;
        reducePeakCount(ulsDirections_reduced, ulsBorderNorms_reduced, intensities, detectorPeaks_m);

        if (threadCount == 1) //threads from crystfel (--pinkIndexer_thread_count)
        {
            sinogram.computeSinogram(ulsDirections_reduced, ulsBorderNorms_reduced);
        }
        else if (threadCount < 32)
        {
            sinogram.computeSinogramParallel(ulsDirections_reduced, ulsBorderNorms_reduced, threadCount);
        }
        else // probably not ran in parellel to other instances
        {
            int slaveThreadCount = threadCount - 1;
            sinogram.computeSinogramParallel2(ulsDirections_reduced, ulsBorderNorms_reduced, slaveThreadCount);
        }

        AngleAxisf bestRotation;
        sinogram.getBestRotation(bestRotation);

        Matrix3f bestBasis = bestRotation * sampleLattice.getBasis();
        indexedLattice = Lattice(bestBasis);

        refine(indexedLattice, centerShift, ulsDirections, ulsBorderNorms, detectorPeaks_m, threadCount);

        indexedLattice.minimize();
        indexedLattice.reorder(sampleLattice);  //reorder lattice vectors to match sample lattice (from crystfel)

		// return how many peaks have been fitted correctly (according to tolerance)
        return refinement.getFittedPeaks(indexedLattice, fittedPeaks, ulsDirections, ulsBorderNorms);

        // sinogram.saveToFile("C:\\DesyFiles\\workspaces\\VisualStudio_workspace\\pinkIndexer\\workfolder\\sinogram");
    }

    void PinkIndexer::refine(Lattice& indexedLattice, Vector2f& centerShift, const Matrix3Xf& ulsDirections, const Array2Xf& ulsBorderNorms,
                             const Matrix2Xf& detectorPeaks_m, int threadCount)
    {
        centerShift.setZero();

        switch (refinementType)
        {
            case RefinementType::none:
                break;
            case RefinementType::fixedLatticeParameters:
                refinement.setTolerance(min(finalRefinementTolerance * 2.0, 0.12));
                refinement.refineFixedLattice(indexedLattice, ulsDirections, ulsBorderNorms);
                refinement.setTolerance(finalRefinementTolerance);
                refinement.refineFixedLattice(indexedLattice, ulsDirections, ulsBorderNorms);
                break;
            case RefinementType::variableLatticeParameters:
                refinement.setTolerance(min(finalRefinementTolerance * 2.0, 0.12));
                refinement.refineVariableLattice(indexedLattice, ulsDirections, ulsBorderNorms);
                refinement.setTolerance(finalRefinementTolerance);
                refinement.refineVariableLattice(indexedLattice, ulsDirections, ulsBorderNorms);
                break;
            case RefinementType::firstFixedThenVariableLatticeParameters:
                refinement.setTolerance(min(finalRefinementTolerance * 2.5, 0.12));
                refinement.refineFixedLattice(indexedLattice, ulsDirections, ulsBorderNorms);
                refinement.setTolerance(min(finalRefinementTolerance * 1.8, 0.10));
                refinement.refineVariableLattice(indexedLattice, ulsDirections, ulsBorderNorms);
                refinement.setTolerance(finalRefinementTolerance);
                refinement.refineVariableLattice(indexedLattice, ulsDirections, ulsBorderNorms);
                break;
            case RefinementType::firstFixedThenVariableLatticeParametersMultiSeed:
            {
                constexpr int refinementTries = 1000;  //TODO: increase if better refinement needed
                int fittedNodesCount[refinementTries];
                double fittedNodesMeanDefects[refinementTries];
                Lattice fittedLattices[refinementTries];

                float maxRelativeDeviation = 0.0125;	//TODO: Parameter??
                Array<float, 1, 3> columnDeviationNorms = indexedLattice.getBasis().colwise().norm() * maxRelativeDeviation;

#ifdef OPENMP_AVAILABLE
                omp_set_num_threads(threadCount);
#endif
#pragma omp parallel for
                for (int i = 0; i < refinementTries; ++i)
                {
                    Refinement refinement(finalRefinementTolerance);

                    Matrix3f currentBasis;
                    if (i > 0)
                    {
                        currentBasis = indexedLattice.getBasis() + (Array33f::Random().rowwise() * columnDeviationNorms).matrix();
                    }
                    else
                    {
                        currentBasis = indexedLattice.getBasis();
                    }
                    fittedLattices[i] = Lattice(currentBasis);

                    refinement.setTolerance(min(finalRefinementTolerance * 2.5, 0.12));
                    refinement.refineFixedLattice(fittedLattices[i], ulsDirections, ulsBorderNorms);
                    refinement.setTolerance(min(finalRefinementTolerance * 1.8, 0.10));
                    refinement.refineVariableLattice(fittedLattices[i], ulsDirections, ulsBorderNorms);
                    refinement.setTolerance(finalRefinementTolerance);
                    refinement.refineVariableLattice(fittedLattices[i], ulsDirections, ulsBorderNorms);

                    fittedNodesCount[i] = refinement.getFittedPeaksCount(fittedLattices[i], ulsDirections, ulsBorderNorms);
                    fittedNodesMeanDefects[i] = refinement.getMeanDefect(fittedLattices[i].getBasis(), ulsDirections, ulsBorderNorms);
                }

                int maxFittedNodesCount = 1;
                double minFittedNodesMeanDefect = 1;
                for (int i = 0; i < refinementTries; ++i)
                {
                    // if (fittedNodesCount[i] > maxFittedNodesCount ||
                    //    (fittedNodesCount[i] == maxFittedNodesCount && fittedNodesMeanDefects[i] < minFittedNodesMeanDefect))
                    if (fittedNodesCount[i] / maxFittedNodesCount > 1.2 ||
                        ((fittedNodesCount[i] > maxFittedNodesCount || fittedNodesMeanDefects[i] < minFittedNodesMeanDefect) &&
                         (fittedNodesCount[i] / maxFittedNodesCount - 1) * 3 > (minFittedNodesMeanDefect / fittedNodesMeanDefects[i] - 1)))  //TODO: can be optimized
                    {
                        maxFittedNodesCount = fittedNodesCount[i];
                        minFittedNodesMeanDefect = fittedNodesMeanDefects[i];
                        indexedLattice = fittedLattices[i];
                    }
                }
            }
            break;
            case RefinementType::firstFixedThenVariableLatticeParametersCenterAdjustmentMultiSeed:
            {
                constexpr int refinementTries = 2000;		//TODO: increase if better refinement needed
                int fittedNodesCount[refinementTries];
                double fittedNodesMeanDefects[refinementTries];
                Lattice fittedLattices[refinementTries];
                Vector2f centerShifts[refinementTries];

                float maxRelativeDeviation = 0.0125;
                Array<float, 1, 3> columnDeviationNorms = indexedLattice.getBasis().colwise().norm() * maxRelativeDeviation;

#ifdef OPENMP_AVAILABLE
                omp_set_num_threads(threadCount);
#endif
#pragma omp parallel for
                for (int i = 0; i < refinementTries; ++i)
                {
                    Backprojection backprojection_local = backprojection;
                    Refinement refinement(finalRefinementTolerance, backprojection_local);

                    Matrix3f currentBasis;
                    if (i > 0)
                    {
                        currentBasis = indexedLattice.getBasis() + (Array33f::Random().rowwise() * columnDeviationNorms).matrix();
                    }
                    else
                    {
                        currentBasis = indexedLattice.getBasis();
                    }
                    fittedLattices[i] = Lattice(currentBasis);
                    centerShifts[i] = Vector2f::Random() * 80e-6;  //TODO: hardcoded JUNGFRAU pixel size. Can be improved (maybe parameter??)

                    refinement.setTolerance(min(finalRefinementTolerance * 2.5, 0.12));
                    refinement.refineFixedLattice(fittedLattices[i], ulsDirections, ulsBorderNorms);
                    refinement.setTolerance(min(finalRefinementTolerance * 1.8, 0.10));
                    refinement.refineVariableLatticeWithCenter(fittedLattices[i], centerShifts[i], detectorPeaks_m);
                    refinement.setTolerance(finalRefinementTolerance);
                    refinement.refineVariableLatticeWithCenter(fittedLattices[i], centerShifts[i], detectorPeaks_m);

                    fittedNodesCount[i] = refinement.getFittedPeaksCount(fittedLattices[i], ulsDirections, ulsBorderNorms);
                    fittedNodesMeanDefects[i] = refinement.getMeanDefect(fittedLattices[i].getBasis(), ulsDirections, ulsBorderNorms);
                }

                int maxFittedNodesCount = 1;
                double minFittedNodesMeanDefect = 1;
                for (int i = 0; i < refinementTries; ++i)
                {
                    // if (fittedNodesCount[i] > maxFittedNodesCount ||
                    //    (fittedNodesCount[i] == maxFittedNodesCount && fittedNodesMeanDefects[i] < minFittedNodesMeanDefect))
                    if (fittedNodesCount[i] / maxFittedNodesCount > 1.2 ||
                        ((fittedNodesCount[i] > maxFittedNodesCount || fittedNodesMeanDefects[i] < minFittedNodesMeanDefect) &&
                         (fittedNodesCount[i] / maxFittedNodesCount - 1) * 3 > (minFittedNodesMeanDefect / fittedNodesMeanDefects[i] - 1)))
                    {
                        maxFittedNodesCount = fittedNodesCount[i];
                        minFittedNodesMeanDefect = fittedNodesMeanDefects[i];
                        indexedLattice = fittedLattices[i];
                        centerShift = centerShifts[i];
                    }
                }
            }
            break;
            default:
                break;
        }
    }

    void PinkIndexer::reducePeakCount(Matrix3Xf& ulsDirections, Array2Xf& ulsBorderNorms, RowVectorXf& intensities, const Eigen::Matrix2Xf& detectorPeaks_m)
    {
        Matrix2Xf detectorPeaks_m_copy = detectorPeaks_m;

        // first clear all above resolution limit
        int peaksKept_res = 0;
        for (int i = 0; i < intensities.size(); i++)
        {
            if (ulsBorderNorms(1, i) <= maxResolutionForIndexing_1_per_A)
            {
                ulsDirections.col(peaksKept_res) = ulsDirections.col(i);
                ulsBorderNorms.col(peaksKept_res) = ulsBorderNorms.col(i);
                intensities[peaksKept_res] = intensities[i];
                detectorPeaks_m_copy.col(peaksKept_res) = detectorPeaks_m_copy.col(i);
                peaksKept_res++;
            }
        }
        ulsDirections.conservativeResize(NoChange, peaksKept_res);
        ulsBorderNorms.conservativeResize(NoChange, peaksKept_res);
        intensities.conservativeResize(peaksKept_res);
        detectorPeaks_m_copy.conservativeResize(NoChange, peaksKept_res);

        // then clear some at high and some at low resolution
        int consideredPeaksCount = getConsideredPeaksCount();

        if (consideredPeaksCount >= intensities.size())
            return;

        int peaksToRemoveCount = intensities.size() - consideredPeaksCount;
        int peaksToRemoveByNormMin = min(0.1 * peaksToRemoveCount, 20.0);
        int peaksToRemoveByNormMax = 0.75 * peaksToRemoveCount;
        int peaksToRemoveByIntensity = peaksToRemoveCount - peaksToRemoveByNormMin - peaksToRemoveByNormMax;

        RowVectorXf norms = detectorPeaks_m_copy.colwise().norm();
        RowVectorXf norms_sorted = norms;
        sort((float*)norms_sorted.data(), (float*)norms_sorted.data() + norms_sorted.size());
        float minNorm = norms_sorted[peaksToRemoveByNormMin];
        float maxNorm = norms_sorted[norms_sorted.size() - peaksToRemoveByNormMax - 1];

        int peaksKept_norms = 0;
        for (int i = 0; i < norms.cols(); i++)
        {
            if (norms[i] >= minNorm && norms[i] <= maxNorm)
            {
                ulsDirections.col(peaksKept_norms) = ulsDirections.col(i);
                ulsBorderNorms.col(peaksKept_norms) = ulsBorderNorms.col(i);
                intensities[peaksKept_norms] = intensities[i];
                peaksKept_norms++;
            }
        }

        RowVectorXf intensities_sorted = intensities;
        nth_element((float*)intensities_sorted.data(), (float*)intensities_sorted.data() + peaksToRemoveByIntensity,
                    (float*)intensities_sorted.data() + peaksKept_norms);
        float minIntensity = intensities_sorted[peaksToRemoveByIntensity];

        int peaksKept_normsIntensities = 0;
        for (int i = 0; i < peaksKept_norms; i++)
        {
            if (intensities[i] > minIntensity)
            {
                ulsDirections.col(peaksKept_normsIntensities) = ulsDirections.col(i);
                ulsBorderNorms.col(peaksKept_normsIntensities) = ulsBorderNorms.col(i);
                intensities[peaksKept_normsIntensities] = intensities[i];
                peaksKept_normsIntensities++;
            }
        }

		if (peaksKept_normsIntensities < consideredPeaksCount)
        {
            for (int i = 0; i < peaksKept_norms && peaksKept_normsIntensities < consideredPeaksCount; i++)
            {
                if (intensities[i] == minIntensity)
                {
                    ulsDirections.col(peaksKept_normsIntensities) = ulsDirections.col(i);
                    ulsBorderNorms.col(peaksKept_normsIntensities) = ulsBorderNorms.col(i);
                    intensities[peaksKept_normsIntensities] = intensities[i];
                    peaksKept_normsIntensities++;
                }
            }
        }

        ulsDirections.conservativeResize(NoChange, peaksKept_normsIntensities);
        ulsBorderNorms.conservativeResize(NoChange, peaksKept_normsIntensities);
        intensities.conservativeResize(peaksKept_normsIntensities);
    }

    float PinkIndexer::getAngleResolution()
    {
		// angluar step in sinogram (in degree)
        switch (angleResolution)
        {
            case AngleResolution::extremelyLoose:
                return 1.5;
            case AngleResolution::loose:
                return 1.1;
            case AngleResolution::standard:
                return 0.8;
            case AngleResolution::dense:
                return 0.5;
            case AngleResolution::extremelyDense:
                return 0.3;
            default:
                throw BadInputException("Unknown angle resolution selected");
        }
    }

    int PinkIndexer::getConsideredPeaksCount()
    {
        switch (consideredPeaksCount)
        {
            case ConsideredPeaksCount::veryFew:
                return 30;
            case ConsideredPeaksCount::few:
                return 70;
            case ConsideredPeaksCount::standard:
                return 127;
            case ConsideredPeaksCount::many:
                return 190;
            case ConsideredPeaksCount::manyMany:
                return 255;
            default:
                throw BadInputException("Unknown considered peaks count selected");
        }
    }
} // namespace pinkIndexer