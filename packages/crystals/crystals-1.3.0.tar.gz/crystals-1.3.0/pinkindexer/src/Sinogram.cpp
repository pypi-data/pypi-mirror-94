#define _USE_MATH_DEFINES
#include <cmath>

#include "Sinogram.h"

#include <algorithm>
#include <fstream>
#include <iostream>
#include <limits>
#include <thread>
#include <vector>


using namespace std;
using namespace Eigen;

namespace pinkIndexer
{
    Sinogram::Sinogram(const Lattice& lattice)
        : reflectionsInRangeFinder(lattice)
    {
        angleResolution_deg = -1;
    }

    void Sinogram::setSinogramAngleResolution(float angleResolution_deg)
    {
        if (angleResolution_deg == this->angleResolution_deg)
        {
            return;
        }

        this->angleResolution_deg = angleResolution_deg;

        sinogramSize_exact = ceil(360 / angleResolution_deg / 2) * 2 + 1;
        uint8_t sinogramOversize = 8;
        sinogramSize = sinogramSize_exact + sinogramOversize;

        uint64_t sinogramElementsCount = (uint64_t)sinogramSize * sinogramSize * sinogramSize;
        if (sinogramElementsCount > numeric_limits<uint32_t>::max())
        {
            throw BadInputException("sinogram too big to fit in uint32 adress range!");
        }

        sinogram.resize(sinogramElementsCount, 1);
        sinogram_oneMeasuredPeak.resize(sinogramElementsCount, 1);

        sinogramCenter = sinogramSize / 2;
        sinogramScale = 1 / ((float)sinogramSize_exact / 2);

        realToMatrixScaling = (float)sinogramSize_exact / 2 / atan(M_PI / 4);
        realToMatrixOffset = (float)sinogramSize / 2;

        strides << sinogramSize, sinogramSize * sinogramSize;

        // clang-format off
	Matrix3Xi dilationOffsets_subscripts(3,28);
	dilationOffsets_subscripts << -1,  0,  1, -1,  0,  1, -1,  0,  1, -1,  0,  1, -1,  0,  1, -1,  0,  1, -1,  0,  1, -1,  0,  1, -1,  0,  1, 1,
								  -1, -1, -1,  0,  0,  0,  1,  1,  1, -1, -1, -1,  0,  0,  0,  1,  1,  1, -1, -1, -1,  0,  0,  0,  1,  1,  1, 1,
		                          -1, -1, -1, -1, -1, -1, -1, -1, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,  1,  1,  1,  1,  1, 1;
	dilationOffsets = dilationOffsets_subscripts.cast<uint32_t>().row(0) + strides * dilationOffsets_subscripts.cast<uint32_t>().bottomRows(2);
        // clang-format on

        anglesCount = (uint32_t)(sinogramSize_exact * 0.8) & ~1; // just a guess...
                                                                 // distance between points should be < 3px so that there are no holes in the
                                                                 // sampled lines, & ~1 to make it even
        Array<float, 1, Eigen::Dynamic> rotationAngles = Array<float, 1, Eigen::Dynamic>::LinSpaced(anglesCount, -2 * M_PI, 0);

        sinah = sin(rotationAngles / 2);
        cosah = cos(rotationAngles / 2);
    }


    void Sinogram::computeSinogram(const Eigen::Matrix3Xf& ulsDirections, const Eigen::Matrix2Xf ulsBorderNorms)
    {
        sinogram.setZero();

        EigenSTL::vector_Matrix3Xf candidateReflectionsDirections;	//unit vectors to all candidate reflections
        reflectionsInRangeFinder.getReflectionsInRanges(candidateReflectionsDirections, ulsBorderNorms);	//get candidate reflections

        Matrix3Xf e(3, anglesCount);	//resulting rotation axes
        Array<float, 1, Eigen::Dynamic> thetah(anglesCount); // theta half - resulting rotation angle (around e)
        Matrix<uint32_t, 3, Eigen::Dynamic> validSinogramPoints_matrix(3, anglesCount);		// coordinates (3D) of sampled curve in sinogram
        Matrix<uint32_t, 1, Eigen::Dynamic> validSinogramPoints_matrix_lin(1, anglesCount);	//linear indices (1D) of validSinogramPoints_matrix

        Matrix<uint32_t, 28, 1> validSinogramPoints_matrix_lin_dilated;  //all voxels neigboring one single voxel (in sinogram)

        int measuredPeaksCount = ulsDirections.cols();
        cout << "peak count used for indexing: " << measuredPeaksCount << endl;
        for (int measuredPeakNumber = 0; measuredPeakNumber < measuredPeaksCount; measuredPeakNumber++)
        {
            if (measuredPeakNumber % 16 == 0)
            {
                cout << "computed " << 100 * (float)measuredPeakNumber / measuredPeaksCount << "%" << endl;
            }

            Vector3f q = ulsDirections.col(measuredPeakNumber); 

            Matrix3Xf& candidateReflectionDirections = candidateReflectionsDirections[measuredPeakNumber];
            if (candidateReflectionDirections.cols() == 0)
                continue;

            sinogram_oneMeasuredPeak.setZero();	//sinogram for one Bragg spot (from detector)
            int candidatePeaksCount = candidateReflectionDirections.cols();
            for (int candidatePeakNumber = 0; candidatePeakNumber < candidatePeaksCount; candidatePeakNumber++)	//calculation of curves for each candidate peak
            {
                const auto& h = candidateReflectionDirections.col(candidatePeakNumber);

                Vector3f m = (h + q).normalized();

                thetah = acos(sinah * (-q.dot(m)));
                e = (m * cosah.matrix() + q.cross(m) * sinah.matrix()).array().rowwise() / sin(thetah);

                Matrix3Xf& validSinogramPoints = e; // memory reuse
                validSinogramPoints = (e.array().rowwise() * atan(thetah / 2)).matrix();

                validSinogramPoints_matrix = ((validSinogramPoints * realToMatrixScaling).array() + realToMatrixOffset).matrix().cast<uint32_t>();
                validSinogramPoints_matrix_lin = validSinogramPoints_matrix.row(0) + strides * validSinogramPoints_matrix.bottomRows(2);

				// for each point from the curve, dilate it and insert into sinogram
                for (uint32_t *linIdx = validSinogramPoints_matrix_lin.data(),
                              *end = validSinogramPoints_matrix_lin.data() + validSinogramPoints_matrix_lin.size();
                     linIdx < end; linIdx++)
                {
                    validSinogramPoints_matrix_lin_dilated = *linIdx + dilationOffsets.array();
                    for (uint32_t *linIdx_dilated = validSinogramPoints_matrix_lin_dilated.data(), *end = validSinogramPoints_matrix_lin_dilated.data() + 27;
                         linIdx_dilated < end; linIdx_dilated++)
                    {
                        sinogram_oneMeasuredPeak[*linIdx_dilated] = 1;
                    }
                }
            }

            sinogram += sinogram_oneMeasuredPeak;
        }
    }

    void Sinogram::computePartOfSinogramOnePeak(Matrix3Xf* candidateReflectionDirections, Vector3f* q, int threadCount, int threadNumber)
    {
        Matrix3Xf e(3, anglesCount);
        Array<float, 1, Eigen::Dynamic> thetah(anglesCount);	//theta half
        Matrix<uint32_t, 3, Eigen::Dynamic> validSinogramPoints_matrix(3, anglesCount);
        Matrix<uint32_t, 1, Eigen::Dynamic> validSinogramPoints_matrix_lin(1, anglesCount);

        Matrix<uint32_t, 28, 1> validSinogramPoints_matrix_lin_dilated;

        Matrix3Xf temp1(3, anglesCount);
        Array<float, 1, Eigen::Dynamic> temp2;

        int candidatePeaksCount = candidateReflectionDirections->cols();
        for (int candidatePeakNumber = threadNumber; candidatePeakNumber < candidatePeaksCount; candidatePeakNumber += threadCount)
        {
            const auto& h = candidateReflectionDirections->col(candidatePeakNumber);

            Vector3f m = (h + *q).normalized();

            temp2 = sinah * (-q->dot(m));
            thetah = acos(temp2);
            temp1.noalias() = m * cosah.matrix();
            temp1.noalias() += q->cross(m) * sinah.matrix();
            e = temp1.array().rowwise() * rsqrt(1 - temp2.square());
            // thetah = acos(sinah * (-q->dot(m)));
            // e = (m * cosah.matrix() + q->cross(m) * sinah.matrix()).array().rowwise() / sin(thetah);

            Matrix3Xf& validSinogramPoints = e; // memory reuse
            validSinogramPoints = (e.array().rowwise() * atan(thetah / 2)).matrix();

            validSinogramPoints_matrix = ((validSinogramPoints * realToMatrixScaling).array() + realToMatrixOffset).matrix().cast<uint32_t>();
            validSinogramPoints_matrix_lin = validSinogramPoints_matrix.row(0);
            validSinogramPoints_matrix_lin.noalias() += strides * validSinogramPoints_matrix.bottomRows(2);

            for (uint32_t *linIdx = validSinogramPoints_matrix_lin.data(), *end = validSinogramPoints_matrix_lin.data() + validSinogramPoints_matrix_lin.size();
                 linIdx < end; linIdx++)
            {
                validSinogramPoints_matrix_lin_dilated = *linIdx + dilationOffsets.array();
                for (uint32_t *linIdx_dilated = validSinogramPoints_matrix_lin_dilated.data(), *end = validSinogramPoints_matrix_lin_dilated.data() + 27;
                     linIdx_dilated < end; linIdx_dilated++)
                {
                    sinogram_oneMeasuredPeak[*linIdx_dilated] = 1;
                }
            }
        }
    }

    // workers create sinogram_onePixel, master adds it to sinogram
    void Sinogram::computeSinogramParallel(const Eigen::Matrix3Xf& ulsDirections, const Eigen::Matrix2Xf ulsBorderNorms, int slaveThreadCount)
    {
        vector<thread> threads;
        threads.reserve(slaveThreadCount);

        sinogram.setZero();

        EigenSTL::vector_Matrix3Xf candidateReflectionsDirections;
        reflectionsInRangeFinder.getReflectionsInRanges(candidateReflectionsDirections, ulsBorderNorms);

        int measuredPeaksCount = ulsDirections.cols();
        cout << "peak count used for indexing: " << measuredPeaksCount << endl;
        for (int measuredPeakNumber = 0; measuredPeakNumber < measuredPeaksCount; measuredPeakNumber++)
        {
            if (measuredPeakNumber % 16 == 0)
            {
                cout << "computed " << 100 * (float)measuredPeakNumber / measuredPeaksCount << "%" << endl;
            }

            Vector3f q = ulsDirections.col(measuredPeakNumber); // rotation axis

            Matrix3Xf& candidateReflectionDirections = candidateReflectionsDirections[measuredPeakNumber];
            if (candidateReflectionDirections.cols() == 0)
                continue;

            sinogram_oneMeasuredPeak.setZero();

            for (int threadNumber = 0; threadNumber < slaveThreadCount; threadNumber++)
            {
                threads.push_back(thread(&Sinogram::computePartOfSinogramOnePeak, this, &candidateReflectionDirections, &q, slaveThreadCount, threadNumber));
            }
            for (int threadNumber = 0; threadNumber < slaveThreadCount; threadNumber++)
            {
                threads[threadNumber].join();
            }
            threads.clear();

            sinogram += sinogram_oneMeasuredPeak;
        }
    }

    // workers create sinogram_onePixel, master changes the buffers, starts new computation and adds it to sinogram in parallel to workers filling the new
    // sinogram_onePixel. Needs zeroing 2 buffers instead of 1, but avoids master as bottleneck
    void Sinogram::computeSinogramParallel2(const Eigen::Matrix3Xf& ulsDirections, const Eigen::Matrix2Xf ulsBorderNorms, int slaveThreadCount)
    {
        vector<thread> threads;
        threads.reserve(slaveThreadCount);

        Matrix<uint8_t, Eigen::Dynamic, 1> sinogram_oneMeasuredPeak_local(sinogram_oneMeasuredPeak.size(), 1);
        sinogram_oneMeasuredPeak_local.setZero();

        sinogram.setZero();

        EigenSTL::vector_Matrix3Xf candidateReflectionsDirections;
        reflectionsInRangeFinder.getReflectionsInRanges(candidateReflectionsDirections, ulsBorderNorms);

        int measuredPeaksCount = ulsDirections.cols();
        cout << "peak count used for indexing: " << measuredPeaksCount << endl;
        for (int measuredPeakNumber = 0; measuredPeakNumber < measuredPeaksCount; measuredPeakNumber++)
        {
            if (measuredPeakNumber % 16 == 0)
            {
                cout << "computed " << 100 * (float)measuredPeakNumber / measuredPeaksCount << "%" << endl;
            }

            Vector3f q = ulsDirections.col(measuredPeakNumber); 

            Matrix3Xf& candidateReflectionDirections = candidateReflectionsDirections[measuredPeakNumber];
            if (candidateReflectionDirections.cols() == 0)
                continue;

            sinogram_oneMeasuredPeak.setZero();

            for (int threadNumber = 0; threadNumber < slaveThreadCount; threadNumber++)
            {
                threads.push_back(thread(&Sinogram::computePartOfSinogramOnePeak, this, &candidateReflectionDirections, &q, slaveThreadCount, threadNumber));
            }

            if (measuredPeakNumber > 0)
            {
                sinogram += sinogram_oneMeasuredPeak_local;
                sinogram_oneMeasuredPeak_local.setZero();
            }

            for (int threadNumber = 0; threadNumber < slaveThreadCount; threadNumber++)
            {
                threads[threadNumber].join();
            }
            threads.clear();

            sinogram_oneMeasuredPeak_local.swap(sinogram_oneMeasuredPeak);
        }
        sinogram += sinogram_oneMeasuredPeak_local;
    }

    void Sinogram::getBestRotation(AngleAxisf& bestRotation)
    {
        uint32_t maxElementIdx, dummy;
        sinogram.maxCoeff(&maxElementIdx, &dummy);

        Matrix<uint32_t, 3, 1> maxElementSub;
        maxElementSub(2) = maxElementIdx / strides(1);
        maxElementIdx -= maxElementSub(2) * strides(1);
        maxElementSub(1) = maxElementIdx / strides(0);
        maxElementSub(0) = maxElementIdx - maxElementSub(1) * strides(0);

		// TODO: might be improved by proper search of centor of mass
        Vector3f centerOfMassSub_f;
        Matrix<uint32_t, 3, 1> centerOfMassSub, oldCenterOfMassSub = maxElementSub;
        int maxIterationCount = 5;
        for (int iteration = 0; iteration < maxIterationCount; iteration++)
        {
            getLocalCenterOfMass(centerOfMassSub_f, oldCenterOfMassSub);
            centerOfMassSub = centerOfMassSub_f.array().round().matrix().cast<uint32_t>();
            if ((oldCenterOfMassSub - centerOfMassSub).isZero(0))
                break;
            oldCenterOfMassSub = centerOfMassSub;
        }

		// calculation from siogram coordinates to vector coordinates
        Vector3f bestRotationVector = centerOfMassSub_f - Vector3f(sinogramCenter, sinogramCenter, sinogramCenter);
        Vector3f bestAxis = bestRotationVector.normalized();
        float bestAngle = tan(bestRotationVector.norm() * sinogramScale * atan(M_PI / 4)) * 4;

        bestRotation = AngleAxisf(bestAngle, bestAxis);
    }

    void Sinogram::getLocalCenterOfMass(Vector3f& centerOfMassSub, const Matrix<uint32_t, 3, 1>& centerElementSub)
    {
        Matrix<uint32_t, 3, 1> currentElementSub;
        vector<Matrix<uint32_t, 3, 1>> validScaledSubs;
        vector<float> validIntensities, validIntensities_copy;
        validScaledSubs.reserve(5 * 5 * 5);
        validIntensities.reserve(5 * 5 * 5);

        Matrix<uint32_t, 3, 1> summedScaledSubs;
        summedScaledSubs.setZero();
        float summedIntensities = 0;

        for (int z = -2; z <= 2; z++)
        {
            currentElementSub[2] = centerElementSub[2] + z;
            if (currentElementSub[2] >= sinogramSize)
                continue;

            uint32_t linIndexZ = strides[1] * currentElementSub[2];
            for (int y = -2; y <= 2; y++)
            {
                currentElementSub[1] = centerElementSub[1] + y;
                if (currentElementSub[1] >= sinogramSize)
                    continue;

                uint32_t linIndexY = linIndexZ + strides[0] * currentElementSub[1];
                for (int x = -2; x <= 2; x++)
                {
                    currentElementSub[0] = centerElementSub[0] + x;
                    if (currentElementSub[0] >= sinogramSize)
                        continue;

                    uint32_t linIndex = linIndexY + currentElementSub[0];

                    validScaledSubs.emplace_back(sinogram[linIndex] * currentElementSub);
                    validIntensities.push_back(sinogram[linIndex]);
                }
            }
        }

        validIntensities_copy = validIntensities;

        const auto minIntensityToConsider_it = validIntensities_copy.begin() + validIntensities_copy.size() * 0.7;
        nth_element(validIntensities_copy.begin(), minIntensityToConsider_it, validIntensities_copy.end());
        float minIntensityToConsider = *minIntensityToConsider_it;

        for (uint32_t i = 0; i < validIntensities.size(); ++i)
        {
            if (validIntensities[i] >= minIntensityToConsider)
            {
                summedScaledSubs += validScaledSubs[i];
                summedIntensities += validIntensities[i];
            }
        }

        centerOfMassSub = summedScaledSubs.cast<float>() / summedIntensities;
    }

    void Sinogram::saveToFile(std::string fileName)
    {
        ofstream myfile(fileName, ios::binary);
        myfile.write((const char*)sinogram.data(), sinogram.size());
        myfile.close();
    }
} // namespace pinkIndexer