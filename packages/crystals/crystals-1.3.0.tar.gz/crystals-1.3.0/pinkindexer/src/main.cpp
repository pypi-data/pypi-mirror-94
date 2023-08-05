
#define EIGEN_DONT_PARALLELIZE

#include "Chronometer.h"
#include <Eigen/Dense>
#include <iostream>

#include "tests.h"

using namespace std;
using namespace Eigen;
using namespace pinkIndexer;
int main()
{
    Eigen::initParallel();

    try
    {
        // testSimpleProjection();
        // testBackprojection();
        // testReflectionsInRangeFinder();
        // testSinogram();
        // testSinogram2();
        testSinogramComplete();
        // testRefinementGetDefect();
        //testRefinement();
        // testPatternPrediction();
        // testPinkIndexer();
    }
    catch (exception& e)
    {
        cout << e.what();
    }

    cout << endl << endl << "done!";
    getchar();

    return 0;
}
