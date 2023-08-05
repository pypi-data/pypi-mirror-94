#define _USE_MATH_DEFINES
#include <cmath>

#include "Refinement.h"
#include "WrongUsageException.h"
#include "eigenSTLContainers.h"
#include <iostream>
#include <limits>

using namespace std;
using namespace Eigen;

namespace pinkIndexer
{
    static void roundTowardsZero(Matrix3Xf& x);
    static void roundAwayFromZero(Matrix3Xf& x);

    Refinement::Refinement(float tolerance)
        : tolerance(tolerance)
    {
        millerIndices.reserve(500);
        backprojection = NULL;
    }

    Refinement::Refinement(float tolerance, const Backprojection& backprojection)
        : tolerance(tolerance)
        , backprojection(&backprojection)
    {
        millerIndices.reserve(500);
    }

    void Refinement::refineVariableLattice(Lattice& lattice, const Matrix3Xf& ulsDirections, const Array2Xf& ulsBorderNorms)
    {
        Matrix3f basis = lattice.getBasis();
        float delta = 1e-8; //for numerical differentiation, in A^-1

        float stepSize = lattice.getBasisVectorNorms().maxCoeff() * 0.002;
        float minStepSize = lattice.getBasisVectorNorms().minCoeff() * 0.00001;
        int maxStepsCount = 200;
        meanDefects.resize(maxStepsCount);
        meanDefects[0] = getMeanDefect(basis, ulsDirections, ulsBorderNorms);
        for (int i = 0; i < maxStepsCount; i++)
        {
            // cout << meanDefects[i] << endl;

            Array33f gradient; //gradient for change of each basis matrix element
            Matrix3f offsetBasis = basis;
            offsetBasis(0, 0) += delta;
            gradient(0, 0) = getMeanDefect(offsetBasis, ulsDirections, ulsBorderNorms, false) - meanDefects[i];
            offsetBasis(0, 0) = basis(0, 0);
            offsetBasis(1, 0) += delta;
            gradient(1, 0) = getMeanDefect(offsetBasis, ulsDirections, ulsBorderNorms, false) - meanDefects[i];
            offsetBasis(1, 0) = basis(1, 0);
            offsetBasis(2, 0) += delta;
            gradient(2, 0) = getMeanDefect(offsetBasis, ulsDirections, ulsBorderNorms, false) - meanDefects[i];
            offsetBasis(2, 0) = basis(2, 0);
            offsetBasis(0, 1) += delta;
            gradient(0, 1) = getMeanDefect(offsetBasis, ulsDirections, ulsBorderNorms, false) - meanDefects[i];
            offsetBasis(0, 1) = basis(0, 1);
            offsetBasis(1, 1) += delta;
            gradient(1, 1) = getMeanDefect(offsetBasis, ulsDirections, ulsBorderNorms, false) - meanDefects[i];
            offsetBasis(1, 1) = basis(1, 1);
            offsetBasis(2, 1) += delta;
            gradient(2, 1) = getMeanDefect(offsetBasis, ulsDirections, ulsBorderNorms, false) - meanDefects[i];
            offsetBasis(2, 1) = basis(2, 1);
            offsetBasis(0, 2) += delta;
            gradient(0, 2) = getMeanDefect(offsetBasis, ulsDirections, ulsBorderNorms) - meanDefects[i];
            offsetBasis(0, 2) = basis(0, 2);
            offsetBasis(1, 2) += delta;
            gradient(1, 2) = getMeanDefect(offsetBasis, ulsDirections, ulsBorderNorms) - meanDefects[i];
            offsetBasis(1, 2) = basis(1, 2);
            offsetBasis(2, 2) += delta;
            gradient(2, 2) = getMeanDefect(offsetBasis, ulsDirections, ulsBorderNorms) - meanDefects[i];

            float norm = gradient.matrix().norm();
            gradient = gradient / norm * stepSize;
            if (norm == 0)
            {
                // throw WrongUsageException("Numerical problems! Delta has been chosen too small for current lattice!\n");
                break;
            }

            basis = basis - gradient.matrix();
            meanDefects[i + 1] = getMeanDefect(basis, ulsDirections, ulsBorderNorms);

            if (meanDefects[i + 1] > meanDefects[i])
            {
                stepSize = stepSize * 0.9;

                if (i > 10 && (meanDefects.segment(i - 4, 4).maxCoeff() - meanDefects.segment(i - 4, 4).minCoeff()) / meanDefects[i] < 0.01) // settled down
                    stepSize = stepSize * 0.2;

                if (stepSize < minStepSize)
                    break;
            }
        }

        lattice = Lattice(basis);
    }

    void Refinement::refineFixedLattice(Lattice& lattice, const Matrix3Xf& ulsDirections, const Array2Xf& ulsBorderNorms)
    {
        Matrix3f basis = lattice.getBasis();

        float degreeDelta = 0.0001 / 180 * M_PI;
        Matrix3f rotX, rotY, rotZ;
        rotX = AngleAxisf(degreeDelta, Vector3f::UnitX());
        rotY = AngleAxisf(degreeDelta, Vector3f::UnitY());
        rotZ = AngleAxisf(degreeDelta, Vector3f::UnitZ());


        float stepSize = 0.1 / 180 * M_PI;
        float minStepSize = 0.001 / 180 * M_PI;
        int maxStepsCount = 200;
        meanDefects.resize(maxStepsCount);
        meanDefects[0] = getMeanDefect(basis, ulsDirections, ulsBorderNorms);
        for (int i = 0; i < maxStepsCount; i++)
        {
            // cout << meanDefects[i] << endl;

            Vector3f gradient;
            gradient(0) = getMeanDefect(rotX * basis, ulsDirections, ulsBorderNorms) - meanDefects[i];
            gradient(1) = getMeanDefect(rotY * basis, ulsDirections, ulsBorderNorms) - meanDefects[i];
            gradient(2) = getMeanDefect(rotZ * basis, ulsDirections, ulsBorderNorms) - meanDefects[i];

            gradient = -gradient.normalized() * stepSize;
            basis =
                AngleAxisf(gradient(0), Vector3f::UnitX()) * AngleAxisf(gradient(1), Vector3f::UnitY()) * AngleAxisf(gradient(2), Vector3f::UnitZ()) * basis;
            meanDefects[i + 1] = getMeanDefect(basis, ulsDirections, ulsBorderNorms);

            if (meanDefects[i + 1] > meanDefects[i])
            {
                stepSize = stepSize * 0.9;

                if (i > 10 && (meanDefects.segment(i - 4, 4).maxCoeff() - meanDefects.segment(i - 4, 4).minCoeff()) / meanDefects[i] < 0.001) // settled down
                    break;

                if (stepSize < minStepSize)
                    break;
            }
        }

        lattice = Lattice(basis);
    }

    void Refinement::refineVariableLatticeWithCenter(Lattice& lattice, Vector2f& centerShift, const Eigen::Matrix2Xf& detectorPeaks_m)
    {
        Matrix3f basis = lattice.getBasis();
        float delta = 1e-8;

        float stepSize_basis = lattice.getBasisVectorNorms().maxCoeff() * 0.002;
        float minStepSize_basis = lattice.getBasisVectorNorms().minCoeff() * 0.00001;
        float startStepSize_center = 10e-6;
        int maxStepsCount = 200;
        meanDefects.resize(maxStepsCount);
        getCenterShiftedBackprojection(ulsDirections, ulsBorderNorms, detectorPeaks_m, centerShift);
        meanDefects[0] = getMeanDefect(basis, ulsDirections, ulsBorderNorms);
        if (meanDefects[0] == 1)
        {
            return;
        }
        for (int i = 0; i < maxStepsCount; i++)
        {
            // cout << meanDefects[i] << endl;
            if (i % 6 == 0)
            {
                refineCenter(centerShift, basis, detectorPeaks_m, startStepSize_center);
                startStepSize_center *= 0.85;
                getCenterShiftedBackprojection(ulsDirections, ulsBorderNorms, detectorPeaks_m, centerShift);
                meanDefects[i] = getMeanDefect(basis, ulsDirections, ulsBorderNorms);
            }

            Array33f basisGradient;
            Matrix3f offsetBasis = basis;
            offsetBasis(0, 0) += delta;
            basisGradient(0, 0) = getMeanDefect(offsetBasis, ulsDirections, ulsBorderNorms, false) - meanDefects[i];
            offsetBasis(0, 0) = basis(0, 0);
            offsetBasis(1, 0) += delta;
            basisGradient(1, 0) = getMeanDefect(offsetBasis, ulsDirections, ulsBorderNorms, false) - meanDefects[i];
            offsetBasis(1, 0) = basis(1, 0);
            offsetBasis(2, 0) += delta;
            basisGradient(2, 0) = getMeanDefect(offsetBasis, ulsDirections, ulsBorderNorms, false) - meanDefects[i];
            offsetBasis(2, 0) = basis(2, 0);
            offsetBasis(0, 1) += delta;
            basisGradient(0, 1) = getMeanDefect(offsetBasis, ulsDirections, ulsBorderNorms, false) - meanDefects[i];
            offsetBasis(0, 1) = basis(0, 1);
            offsetBasis(1, 1) += delta;
            basisGradient(1, 1) = getMeanDefect(offsetBasis, ulsDirections, ulsBorderNorms, false) - meanDefects[i];
            offsetBasis(1, 1) = basis(1, 1);
            offsetBasis(2, 1) += delta;
            basisGradient(2, 1) = getMeanDefect(offsetBasis, ulsDirections, ulsBorderNorms, false) - meanDefects[i];
            offsetBasis(2, 1) = basis(2, 1);
            offsetBasis(0, 2) += delta;
            basisGradient(0, 2) = getMeanDefect(offsetBasis, ulsDirections, ulsBorderNorms) - meanDefects[i];
            offsetBasis(0, 2) = basis(0, 2);
            offsetBasis(1, 2) += delta;
            basisGradient(1, 2) = getMeanDefect(offsetBasis, ulsDirections, ulsBorderNorms) - meanDefects[i];
            offsetBasis(1, 2) = basis(1, 2);
            offsetBasis(2, 2) += delta;
            basisGradient(2, 2) = getMeanDefect(offsetBasis, ulsDirections, ulsBorderNorms) - meanDefects[i];

            float norm = basisGradient.matrix().norm();
            basisGradient = basisGradient / norm * stepSize_basis;
            if (norm == 0)
            {
                // throw WrongUsageException("Numerical problems! Delta has been chosen too small for current lattice!\n");
                break;
            }

            basis = basis - basisGradient.matrix();
            meanDefects[i + 1] = getMeanDefect(basis, ulsDirections, ulsBorderNorms);

            if (meanDefects[i + 1] > meanDefects[i])
            {
                stepSize_basis = stepSize_basis * 0.9;

                if (i > 10 && (meanDefects.segment(i - 4, 4).maxCoeff() - meanDefects.segment(i - 4, 4).minCoeff()) / meanDefects[i] < 0.01)
                { // settled down
                    stepSize_basis = stepSize_basis * 0.2;
                }

                if (stepSize_basis < minStepSize_basis)
                    break;
            }
        }

        lattice = Lattice(basis);
    }

    void Refinement::refineCenter(Eigen::Vector2f& centerShift, const Matrix3f& basis, const Eigen::Matrix2Xf& detectorPeaks_m, float startStepSize)
    {
        float deltaCenterShift = 1e-7;

        float minStepSize_center = 5e-7;
        float stepSize_center = max(startStepSize, minStepSize_center);


        int maxStepsCount = 35;
        meanDefects_centerAdjustment.resize(maxStepsCount);
        getCenterShiftedBackprojection(ulsDirections, ulsBorderNorms, detectorPeaks_m, centerShift);
        meanDefects_centerAdjustment[0] = getMeanDefect(basis, ulsDirections, ulsBorderNorms);
        if (meanDefects_centerAdjustment[0] == 1)
        {
            return;
        }
        for (int i = 0; i < maxStepsCount; i++)
        {
            // cout << meanDefects[i] << endl;

            Vector2f centerOffsetGradient;
            Vector2f offsetCenterShift = centerShift + Vector2f(deltaCenterShift, 0);
            getCenterShiftedBackprojection(ulsDirections, ulsBorderNorms, detectorPeaks_m, offsetCenterShift);
            centerOffsetGradient.x() = getMeanDefect(basis, ulsDirections, ulsBorderNorms) - meanDefects_centerAdjustment[i];
            offsetCenterShift = centerShift + Vector2f(0, deltaCenterShift);
            getCenterShiftedBackprojection(ulsDirections, ulsBorderNorms, detectorPeaks_m, offsetCenterShift);
            centerOffsetGradient.y() = getMeanDefect(basis, ulsDirections, ulsBorderNorms) - meanDefects_centerAdjustment[i];

            float norm = centerOffsetGradient.norm();
            centerOffsetGradient = centerOffsetGradient / norm * stepSize_center;
            if (norm == 0)
            {
                // throw WrongUsageException("Numerical problems! Delta has been chosen too small for current lattice!\n");
                break;
            }

            centerShift = centerShift - centerOffsetGradient;
            getCenterShiftedBackprojection(ulsDirections, ulsBorderNorms, detectorPeaks_m, centerShift);
            meanDefects_centerAdjustment[i + 1] = getMeanDefect(basis, ulsDirections, ulsBorderNorms);

            if (meanDefects_centerAdjustment[i + 1] > meanDefects_centerAdjustment[i])
            {
                stepSize_center = stepSize_center * 0.8;

                if (i > 5 && (meanDefects_centerAdjustment.segment(i - 4, 4).maxCoeff() - meanDefects_centerAdjustment.segment(i - 4, 4).minCoeff()) /
                                     meanDefects_centerAdjustment[i] <
                                 0.01)
                { // settled down
                    stepSize_center = stepSize_center * 0.2;
                }

                if (stepSize_center < minStepSize_center)
                    break;
            }
        }
    }

    int Refinement::getFittedPeaksCount(Lattice& lattice, const Eigen::Matrix3Xf& ulsDirections, const Eigen::Array2Xf& ulsBorderNorms)
    {
        getDefects(defects, lattice.getBasis(), ulsDirections, ulsBorderNorms);
        int fittedPeaksCount = (defects < tolerance).count();

        return fittedPeaksCount;
    }

    int Refinement::getFittedPeaks(Lattice& lattice, Eigen::Array<bool, Eigen::Dynamic, 1>& fittedPeaks, const Eigen::Matrix3Xf& ulsDirections,
                                   const Eigen::Array2Xf& ulsBorderNorms)
    {
        getDefects(defects, lattice.getBasis(), ulsDirections, ulsBorderNorms);
        fittedPeaks = (defects < tolerance);

        return fittedPeaks.count();
    }


    void Refinement::getDefects(ArrayXf& defects, const Matrix3f& basis, const Matrix3Xf& ulsDirections, const Array2Xf& ulsBorderNorms,
                                bool significantChangesToPreviousCall)
    {
        Matrix3f basis_inverse = basis.inverse();

        if (significantChangesToPreviousCall)
        {
            ulsBorderNormsSquared = ulsBorderNorms.array().square().matrix();

            millerIndices_close = basis_inverse * (ulsDirections.array().rowwise() * ulsBorderNorms.array().row(0)).matrix();
            roundTowardsZero(millerIndices_close);
            millerIndices_far = basis_inverse * (ulsDirections.array().rowwise() * ulsBorderNorms.array().row(1)).matrix();
            roundAwayFromZero(millerIndices_far);
        }

        int peakCount = ulsDirections.cols();
        defects.resize(peakCount);
        for (int i = 0; i < peakCount; i++)
        {
            // create miller indices close to ULS
            millerIndices.clear();
            for (float k = min(millerIndices_close(0, i), millerIndices_far(0, i)), maxK = max(millerIndices_close(0, i), millerIndices_far(0, i)); k <= maxK;
                 k++)
            {
                for (float l = min(millerIndices_close(1, i), millerIndices_far(1, i)), maxL = max(millerIndices_close(1, i), millerIndices_far(1, i));
                     l <= maxL; l++)
                {
                    for (float m = min(millerIndices_close(2, i), millerIndices_far(2, i)), maxM = max(millerIndices_close(2, i), millerIndices_far(2, i));
                         m <= maxM; m++)
                    {
                        millerIndices.emplace_back(k, l, m);
                    }
                }
            }

            candidatePeaks.noalias() = basis * Map<Matrix3Xf>((float*)millerIndices.data(), 3, millerIndices.size());
            candidatePeaksNormsSquared = candidatePeaks.colwise().squaredNorm();
            // clear peaks that exceed the borders
            validCandidatePeaksCount = 0;
            for (int j = 0, end = candidatePeaksNormsSquared.size(); j < end; j++)
            {
                if ((candidatePeaksNormsSquared(j) > ulsBorderNormsSquared(0, i)) & (candidatePeaksNormsSquared(j) < ulsBorderNormsSquared(1, i)))
                {
                    candidatePeaks.col(validCandidatePeaksCount) = candidatePeaks.col(j);
                    validCandidatePeaksCount++;
                }
            }
            if (validCandidatePeaksCount == 0)
            {
                defects(i) = 1;
                continue;
            }

            projectedVectorNorms.noalias() = candidatePeaks.leftCols(validCandidatePeaksCount).transpose() * ulsDirections.col(i);
            defectVectors_absolute = candidatePeaks.leftCols(validCandidatePeaksCount);
            defectVectors_absolute.noalias() -= ulsDirections.col(i) * projectedVectorNorms;
            defectVectors_relative.noalias() = basis_inverse * defectVectors_absolute;
            defects(i) = defectVectors_relative.cwiseAbs().colwise().maxCoeff().minCoeff();
        }
    }

    double Refinement::getMeanDefect(const Matrix3f& basis, const Matrix3Xf& ulsDirections, const Array2Xf& ulsBorderNorms,
                                     bool significantChangesToPreviousCall)
    {
        getDefects(defects, basis, ulsDirections, ulsBorderNorms, significantChangesToPreviousCall);

        notPredictablePeaks = defects > tolerance;
        int16_t notPredictablePeaksCount = notPredictablePeaks.count();
        // cout << "np " << notPredictablePeaksCount << endl;

        if (notPredictablePeaksCount == defects.size())
        {
            return 1;
        }

        sort((float*)defects.data(), (float*)defects.data() + defects.size());
        return defects.head(round(0.9 * (defects.size() - notPredictablePeaksCount))).mean();
    }

    void Refinement::getCenterShiftedBackprojection(Eigen::Matrix3Xf& ulsDirections_local, Eigen::Array2Xf& ulsBorderNorms_local,
                                                    const Eigen::Matrix2Xf& detectorPeaks_m, const Eigen::Vector2f& centerShift)
    {
        detectorPeaks_m_shifted = detectorPeaks_m.colwise() + centerShift;
        backprojection->backProject(detectorPeaks_m_shifted, ulsDirections_local, ulsBorderNorms_local);
    }

    static void roundTowardsZero(Matrix3Xf& x)
    {
        x = x.array().abs().floor() * x.array().sign();
    }

    static void roundAwayFromZero(Matrix3Xf& x)
    {
        x = x.array().abs().ceil() * x.array().sign();
    }
} // namespace pinkIndexer