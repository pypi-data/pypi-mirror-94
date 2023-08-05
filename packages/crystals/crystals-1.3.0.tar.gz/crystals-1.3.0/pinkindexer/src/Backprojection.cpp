
#include "Backprojection.h"


using namespace std;
using namespace Eigen;

namespace pinkIndexer
{


    Backprojection::Backprojection(const ExperimentSettings& experimentSettings)
        : experimentSettings(experimentSettings)
    {
    }

    void Backprojection::backProject(const Matrix2Xf& detectorPeaks_m, Matrix3Xf& ulsDirections, Array2Xf& ulsBorderNorms) const
    {
        Matrix3Xf projectionDirections(3, detectorPeaks_m.cols());
        projectionDirections << RowVectorXf::Constant(1, detectorPeaks_m.cols(), experimentSettings.getDetectorDistance_m()), detectorPeaks_m.row(0),
            detectorPeaks_m.row(1);
        projectionDirections.colwise().normalize();

        Matrix3Xf backprojectedPointsClose = projectionDirections * experimentSettings.getReciprocalLambdaLong_1A();
        backprojectedPointsClose.row(0) -= RowVectorXf::Constant(backprojectedPointsClose.cols(), experimentSettings.getReciprocalLambdaLong_1A());
        Matrix3Xf backprojectedPointsFar = projectionDirections * experimentSettings.getReciprocalLambdaShort_1A();
        backprojectedPointsFar.row(0) -= RowVectorXf::Constant(backprojectedPointsFar.cols(), experimentSettings.getReciprocalLambdaShort_1A());

        ulsBorderNorms.resize(2, detectorPeaks_m.cols());
        ulsBorderNorms.row(0) = backprojectedPointsClose.colwise().norm().array() - experimentSettings.getReflectionRadius();
        ulsBorderNorms.row(1) = backprojectedPointsFar.colwise().norm().array() + experimentSettings.getReflectionRadius();

        ulsDirections = backprojectedPointsFar.colwise().normalized();
    }

} // namespace pinkIndexer