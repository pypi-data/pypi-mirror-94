
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <..\..\_impl\include\frc\trajectory\constraint\DifferentialDriveKinematicsConstraint.h>





#include <rpygen/frc__TrajectoryConstraint.hpp>

namespace rpygen {

using namespace frc;


template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
using PyBasefrc__DifferentialDriveKinematicsConstraint = 
    Pyfrc__TrajectoryConstraint<
        PyTrampolineBase
    
    , CxxBase
    >
;

template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
struct Pyfrc__DifferentialDriveKinematicsConstraint : PyBasefrc__DifferentialDriveKinematicsConstraint<PyTrampolineBase, CxxBase> {
    using PyBasefrc__DifferentialDriveKinematicsConstraint<PyTrampolineBase, CxxBase>::PyBasefrc__DifferentialDriveKinematicsConstraint;


using MinMax = frc::TrajectoryConstraint::MinMax;
#ifndef RPYGEN_DISABLE_KMaxVelocity_KRTPose2d_Tcurvature_t_Tmeters_per_second_t
    units::meters_per_second_t MaxVelocity(const Pose2d& pose, units::curvature_t curvature, units::meters_per_second_t velocity) const override {
PYBIND11_OVERRIDE_NAME(PYBIND11_TYPE(units::meters_per_second_t), CxxBase, "maxVelocity", MaxVelocity,pose, curvature, velocity);    }
#endif

#ifndef RPYGEN_DISABLE_KMinMaxAcceleration_KRTPose2d_Tcurvature_t_Tmeters_per_second_t
    MinMax MinMaxAcceleration(const Pose2d& pose, units::curvature_t curvature, units::meters_per_second_t speed) const override {
PYBIND11_OVERRIDE_NAME(PYBIND11_TYPE(MinMax), CxxBase, "minMaxAcceleration", MinMaxAcceleration,pose, curvature, speed);    }
#endif




};

}; // namespace rpygen
