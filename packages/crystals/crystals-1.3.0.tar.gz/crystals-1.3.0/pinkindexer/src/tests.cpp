/*
 * tests.cpp
 *
 *  Created on: 04.05.2017
 *      Author: Yaro
 */


#include "tests.h"


#define _USE_MATH_DEFINES
#include <cmath>

#include <Eigen/Dense>
#include <chrono>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

#include "Backprojection.h"
#include "Chronometer.h"
#include "ExperimentSettings.h"
#include "PinkIndexer.h"
#include "Refinement.h"
#include "ReflectionsInRangeFinder.h"
#include "SimpleDiffractionPatternPrediction.h"
#include "SimpleProjection.h"
#include "Sinogram.h"
#include "eigenDiskImport.h"

using namespace std;
using namespace Eigen;

namespace pinkIndexer
{

    static ExperimentSettings getExperimentSettingCrystfelTutorial();
    static ExperimentSettings getExperimentSettingLysPink();

    void testPinkIndexer()
    {
        ExperimentSettings experimentSettings = getExperimentSettingLysPink();

        Matrix2Xf peaksOnDetector_m;
        RowVectorXf intensities;
        loadEigenMatrixFromDisk(peaksOnDetector_m, "C:\\DesyFiles\\workspaces\\VisualStudio_workspace\\pinkIndexer\\workfolder\\peaksOnDetector_m");
        loadEigenMatrixFromDisk(intensities, "C:\\DesyFiles\\workspaces\\VisualStudio_workspace\\pinkIndexer\\workfolder\\intensities");

        PinkIndexer::ConsideredPeaksCount consideredPeaksCount = PinkIndexer::ConsideredPeaksCount::standard;
        PinkIndexer::AngleResolution angleResolution = PinkIndexer::AngleResolution::standard;
        PinkIndexer::RefinementType refinementType = PinkIndexer::RefinementType::firstFixedThenVariableLatticeParameters;
        float maxResolutionForIndexing_1_per_A = 0.2; // numeric_limits<float>::max();
        Lattice indexedLattice;
        PinkIndexer pinkIndexer(experimentSettings, consideredPeaksCount, angleResolution, refinementType, maxResolutionForIndexing_1_per_A);

        {
            auto tmp = Chronometer("sinogram");
            int threadCount = 6;
            Eigen::Array<bool, Eigen::Dynamic, 1> fittedPeaks;
            Vector2f centerShift;
            pinkIndexer.indexPattern(indexedLattice, centerShift, fittedPeaks, intensities, peaksOnDetector_m, threadCount);
        }

        SimpleDiffractionPatternPrediction simpleDiffractionPatternPrediction(experimentSettings);
        Matrix2Xf predictedPeaks;
        Matrix3Xi millerIndices;
        Matrix3Xf projectionDirections;
        simpleDiffractionPatternPrediction.predictPattern(predictedPeaks, millerIndices, projectionDirections, indexedLattice);
        ofstream myfile2("C:\\DesyFiles\\workspaces\\VisualStudio_workspace\\pinkIndexer\\workfolder\\peaksOnDetectorPredicted_m");
        myfile2 << predictedPeaks;
        myfile2.close();
    }

    void testPatternPrediction()
    {
        ExperimentSettings experimentSettings = getExperimentSettingLysPink();

        SimpleDiffractionPatternPrediction simpleDiffractionPatternPrediction(experimentSettings);

        Lattice lattice = experimentSettings.getSampleReciprocalLattice_1A();
        Matrix3Xf peaksOnEwaldSphere;
        Matrix3Xi millerIndices;
        Matrix3Xf projectionDirections;
        simpleDiffractionPatternPrediction.getPeaksOnEwaldSphere(peaksOnEwaldSphere, millerIndices, lattice);

        ofstream myfile("C:\\DesyFiles\\workspaces\\VisualStudio_workspace\\pinkIndexer\\workfolder\\peaksOnEwaldSphere");
        myfile << peaksOnEwaldSphere;
        myfile.close();

        Matrix2Xf predictedPeaks;
        simpleDiffractionPatternPrediction.predictPattern(predictedPeaks, millerIndices, projectionDirections, lattice);
        ofstream myfile2("C:\\DesyFiles\\workspaces\\VisualStudio_workspace\\pinkIndexer\\workfolder\\peaksOnDetector_m");
        myfile2 << predictedPeaks;
        myfile2.close();
    }

    void testRefinement()
    {
        Matrix2Xf ulsBorderNorms;
        Matrix3Xf ulsDirections;
        Matrix3f basis;
        loadEigenMatrixFromDisk(ulsBorderNorms, "C:\\DesyFiles\\workspaces\\VisualStudio_workspace\\pinkIndexer\\workfolder\\ulsBorderNorms");
        loadEigenMatrixFromDisk(ulsDirections, "C:\\DesyFiles\\workspaces\\VisualStudio_workspace\\pinkIndexer\\workfolder\\ulsDirections");
        loadEigenMatrixFromDisk(basis, "C:\\DesyFiles\\workspaces\\VisualStudio_workspace\\pinkIndexer\\workfolder\\bestFitBasis");

        float tolerance = 0.15;
        Lattice lattice(basis);
        Refinement refinement(tolerance);

        cout << lattice << endl;
        refinement.refineFixedLattice(lattice, ulsDirections, ulsBorderNorms);
        cout << lattice;
        refinement.refineVariableLattice(lattice, ulsDirections, ulsBorderNorms);
        cout << lattice;
    }

    void testRefinementGetDefect()
    {
        // getDefect is a private function. has to be made public, to test...

        // Matrix2Xf ulsBorderNorms;
        // Matrix3Xf ulsDirections;
        // Matrix3f basis;
        // loadEigenMatrixFromDisk(ulsBorderNorms, "C:\\DesyFiles\\workspaces\\VisualStudio_workspace\\pinkIndexer\\workfolder\\ulsBorderNorms");
        // loadEigenMatrixFromDisk(ulsDirections, "C:\\DesyFiles\\workspaces\\VisualStudio_workspace\\pinkIndexer\\workfolder\\ulsDirections");
        // loadEigenMatrixFromDisk(basis, "C:\\DesyFiles\\workspaces\\VisualStudio_workspace\\pinkIndexer\\workfolder\\basis");

        // Refinement refinement;
        // cout << refinement.getDefect(basis, ulsDirections, ulsBorderNorms) << endl;
    }

     void testSinogramComplete()
    {
        Matrix2Xf ulsBorderNorms;
        Matrix3f knownBasis;
        MatrixXf angleResolution_deg_matrix;
        Matrix3Xf ulsDirections;
        loadEigenMatrixFromDisk(ulsBorderNorms, "C:\\DesyFiles\\workspaces\\VisualStudio_workspace\\pinkIndexer\\workfolder\\ulsBorderNorms");
        loadEigenMatrixFromDisk(ulsDirections, "C:\\DesyFiles\\workspaces\\VisualStudio_workspace\\pinkIndexer\\workfolder\\ulsDirections");
        loadEigenMatrixFromDisk(knownBasis, "C:\\DesyFiles\\workspaces\\VisualStudio_workspace\\pinkIndexer\\workfolder\\knownBasis");
        loadEigenMatrixFromDisk(angleResolution_deg_matrix, "C:\\DesyFiles\\workspaces\\VisualStudio_workspace\\pinkIndexer\\workfolder\\angleResolution_deg");
        float angleResolution_deg = angleResolution_deg_matrix(0, 0);

        Lattice knownLattice(knownBasis);

        Sinogram sinogram(knownLattice);
        sinogram.setSinogramAngleResolution(angleResolution_deg);

        {
            auto tmp = Chronometer("sinogram");

            int slaveThreadCount = 3;
            //sinogram.computeSinogram(ulsDirections, ulsBorderNorms);
            sinogram.computeSinogramParallel(ulsDirections, ulsBorderNorms, slaveThreadCount);
        }

        AngleAxisf bestRotation;
        {
            auto tmp = Chronometer("getBestRotation");

            sinogram.getBestRotation(bestRotation);
        }
        cout << bestRotation.angle() << endl << endl << bestRotation.axis();


        sinogram.saveToFile("C:\\DesyFiles\\workspaces\\VisualStudio_workspace\\pinkIndexer\\workfolder\\sinogram");
    }

    void testSinogram2()
    {
        Matrix3Xf ulsDirections(3, 1);
        ulsDirections << Vector3f(1, -2, 4).normalized();

        Array2Xf ranges(2, 1);
        ranges << 3, 5;

        Matrix3f knownBasis;
        knownBasis << 1, 0, 0, 0, 1, 0, 0, 0, 1;

        float angleResolution_deg = 2;


        Lattice knownLattice(knownBasis);

        Sinogram sinogram(knownLattice);
        sinogram.setSinogramAngleResolution(angleResolution_deg);
        sinogram.computeSinogram(ulsDirections, ranges);

        sinogram.saveToFile("C:\\DesyFiles\\workspaces\\VisualStudio_workspace\\pinkIndexer\\workfolder\\sinogram");
    }

    void testSinogram()
    {
        Matrix3Xf ulsDirections(3, 1);
        ulsDirections << Vector3f(1, -2, 4).normalized();

        Array2Xf ranges(2, 1);
        ranges << 3, 5;

        Matrix3f knownBasis;
        knownBasis << 1, 0, 0, 0, 1, 0, 0, 0, 1;

        float angleResolution_deg = 2;

        Lattice knownLattice(knownBasis);
        Sinogram sinogram(knownLattice);
        sinogram.setSinogramAngleResolution(angleResolution_deg);
        sinogram.computeSinogram(ulsDirections, ranges);

        sinogram.saveToFile("C:\\DesyFiles\\workspaces\\VisualStudio_workspace\\pinkIndexer\\workfolder\\sinogram");
    }

    void testReflectionsInRangeFinder()
    {
        Vector3f a(1, 0.2, 0);
        Vector3f b(0, 1, 0.3);
        Vector3f c(0, 0, 2);
        Matrix3f basis;
        basis << a, b, c;
        Lattice sampleReciprocalLattice(basis);

        ReflectionsInRangeFinder reflectionsInRangeFinder(sampleReciprocalLattice);

        Array2Xf ulsBorderNorms(2, 2);
        ulsBorderNorms << 15, 35, 20, 43;

        EigenSTL::vector_Matrix3Xf candidateReflections;
        reflectionsInRangeFinder.getReflectionsInRanges(candidateReflections, ulsBorderNorms);

        stringstream ss;
        for (int i = 0; i < 2; i++)
        {
            ss.str("");
            ss.clear();
            ss << "workfolder/candidates" << i;
            ofstream outfile(ss.str());
            outfile << candidateReflections[i] << endl << endl;
            outfile.close();
        }
    }

    void testBackprojection()
    {

        Vector3f a(1, 0, 0);
        Vector3f b(0, 1, 0);
        Vector3f c(0, 0, 1);
        Matrix3f basis;
        basis << a, b, c;
        Lattice sampleReciprocalLattice(basis);

        float reflectionRadius = 0.1;
        float beamEenergy_eV = 12400; // 1A
        float detectorDistance_m = 5;
        float nonMonochromaticity = 0.3;
        ExperimentSettings experimentSettings =
            ExperimentSettings(beamEenergy_eV, detectorDistance_m, 1, 1, nonMonochromaticity, sampleReciprocalLattice, 0.1, reflectionRadius);

        Backprojection simpleProjection(experimentSettings);

        Matrix2Xf detectorPeaks_m(2, 1);
        detectorPeaks_m << 1, 5;

        Matrix3Xf ulsDirections;
        Array2Xf ulsBorderNorms;

        Matrix2Xf projectedPoints;
        simpleProjection.backProject(detectorPeaks_m, ulsDirections, ulsBorderNorms);

        cout << ulsDirections << endl << endl << ulsBorderNorms;
    }


    void testSimpleProjection()
    {
        float detectorDistance_m = 5;

        Vector3f a(1, 0, 0);
        Vector3f b(0, 1, 0);
        Vector3f c(0, 0, 1);
        Matrix3f basis;
        basis << a, b, c;
        Lattice sampleReciprocalLattice(basis);
        ExperimentSettings experimentSettings = ExperimentSettings(1, detectorDistance_m, 1, 1, 1, sampleReciprocalLattice, 0.1, 1);

        SimpleProjection simpleProjection(experimentSettings);

        Matrix3Xf reciprocalPeaks(3, 1);
        reciprocalPeaks << -2, 1, 4;

        Matrix2Xf projectedPeaks;
        simpleProjection.project(projectedPeaks, reciprocalPeaks);

        cout << projectedPeaks;
    }


    static ExperimentSettings getExperimentSettingCrystfelTutorial()
    {
        float coffset_m = 582.00e-3;
        float clen_mm = -429.9966;
        float beamEenergy_eV = 9.5085e+03;
        float divergenceAngle_deg = 0.05 * M_PI / 180;
        float nonMonochromaticity = 0.005;
        float pixelLength_m = 110e-6;
        float detectorRadius_pixel = 1750;

        Vector3f a(61.7, 0, 0);
        Vector3f b(0, 122.80, 0);
        Vector3f c(0, 0, 168.1);
        Matrix3f basis;
        basis << a, b, c;
        Lattice sampleLattice_A(basis);
        float tolerance = 0.02;
        float reflectionRadius_1_per_A = 0.5;

        return ExperimentSettings(coffset_m, clen_mm, beamEenergy_eV, divergenceAngle_deg, nonMonochromaticity, pixelLength_m, detectorRadius_pixel,
                                  sampleLattice_A.getReciprocalLattice(), tolerance, reflectionRadius_1_per_A);
    }

    static ExperimentSettings getExperimentSettingLysPink()
    {
        float detectorDistance_m = 0.250000000000000;
        float beamEenergy_eV = 1.0876e+4;
        float divergenceAngle_deg = 0.001745329251994;
        float nonMonochromaticity = 0.250000000000000;
        float detectorRadius_m = 0.115180000000000;

        Vector3f aStar(0.0126422250316056, 0, 0);
        Vector3f bStar(0, 0.0126422250316056, 0);
        Vector3f cStar(0, 0, 0.0263157894736842);
        Matrix3f basis;
        basis << aStar, bStar, cStar;
        Lattice sampleReciprocalLattice_1A(basis);
        float tolerance = 0.01;
        float reflectionRadius_1_per_A = 2.528445006321113e-04;


        return ExperimentSettings(beamEenergy_eV, detectorDistance_m, detectorRadius_m, divergenceAngle_deg, nonMonochromaticity, sampleReciprocalLattice_1A,
                                  tolerance, reflectionRadius_1_per_A);
    }
} // namespace pinkIndexer