#include "ReflectionsInRangeFinder.h"

#include <algorithm>
#include <numeric>
//#include <execution>   //only with c++17 support: 
    
using namespace std;
using namespace Eigen;

namespace pinkIndexer
{
    ReflectionsInRangeFinder::ReflectionsInRangeFinder(const Lattice& lattice)
    {
        const Matrix3f basis = lattice.getBasis();

        int maxMillerIndex = 175;
        maxRadius = maxMillerIndex * lattice.getBasisVectorNorms().minCoeff();
        int millerIndicesPerDirection = 2 * maxMillerIndex + 1;
        Matrix3Xf reflections(3, (int)pow(millerIndicesPerDirection, 3));
        int peakCount = 0;
        for (float i = -maxMillerIndex; i <= maxMillerIndex; i++)
        {
            for (float j = -maxMillerIndex; j <= maxMillerIndex; j++)
            {
                for (float k = -maxMillerIndex; k <= maxMillerIndex; k++)
                {
                    reflections.col(peakCount++) = basis * Vector3f(i, j, k);
                }
            }
        }

        RowVectorXf norms = reflections.colwise().norm();

        vector<uint32_t> sortIndices;
        sortIndices.resize(reflections.cols());
        iota(sortIndices.begin(), sortIndices.end(), 0);
        sort(sortIndices.begin(), sortIndices.end(), [&norms](uint32_t i, uint32_t j) { return norms[i] < norms[j]; });
        //only with c++17 support: 
		//sort(execution::par_unseq, sortIndices.begin(), sortIndices.end(), [&norms](uint32_t i, uint32_t j) { return norms[i] < norms[j]; });

        reflectionsDirections_sorted.resize(3, reflections.cols() - 1); // leave out  reflection (0,0,0)
        norms_sorted.resize(reflections.cols());

        for (int i = 1; i < reflections.cols(); ++i)
        {
            uint32_t sortIndex = sortIndices[i];
            norms_sorted[i] = norms(sortIndex);
            reflectionsDirections_sorted.col(i - 1) = reflections.col(sortIndex) / norms_sorted[i];
        }
    }


    void ReflectionsInRangeFinder::getReflectionsInRanges(EigenSTL::vector_Matrix3Xf& candidateReflectionsDirections, const Array2Xf& ranges)
    {
        if (ranges.row(1).maxCoeff() > maxRadius)
        {
            cerr << "the maximum resolution of Bragg spots exceeds the hardcoded limit of " << maxRadius
                 << "A^-1. These Bragg spots will not be used for indexing, but they will be used for refinement!" << endl;
        }

        candidateReflectionsDirections.resize(ranges.cols());

        for (int i = 0; i < ranges.cols(); i++)
        {
            if (ranges(1, i) > maxRadius)
            {
                candidateReflectionsDirections[i] = Matrix3Xf(3, 0);
            }
            else
            {
                vector<float>::iterator low, up;
                low = lower_bound(norms_sorted.begin(), norms_sorted.end(), ranges(0, i));
                up = upper_bound(norms_sorted.begin(), norms_sorted.end(), ranges(1, i));

                candidateReflectionsDirections[i] = reflectionsDirections_sorted.block(0, low - norms_sorted.begin(), 3, up - low);
            }
        }
    }
} // namespace pinkIndexer