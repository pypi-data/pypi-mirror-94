
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <../../_impl/include/frc/trajectory/constraint/SwerveDriveKinematicsConstraint.h>





#include <rpygen/frc__TrajectoryConstraint.hpp>

namespace rpygen {

using namespace frc;


template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
using PyBasefrc__SwerveDriveKinematicsConstraint = 
    Pyfrc__TrajectoryConstraint<
        PyTrampolineBase
    
    , CxxBase
    >
;

template <typename PyTrampolineBase, size_t NumModules, typename CxxBase = PyTrampolineBase>
struct Pyfrc__SwerveDriveKinematicsConstraint : PyBasefrc__SwerveDriveKinematicsConstraint<PyTrampolineBase, CxxBase> {
    using PyBasefrc__SwerveDriveKinematicsConstraint<PyTrampolineBase, CxxBase>::PyBasefrc__SwerveDriveKinematicsConstraint;


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


namespace rpygen {

using namespace frc;


template <size_t NumModules>
struct bind_frc__SwerveDriveKinematicsConstraint {

          using MinMax = frc::TrajectoryConstraint::MinMax;


      using SwerveDriveKinematicsConstraint_Trampoline = rpygen::Pyfrc__SwerveDriveKinematicsConstraint<typename frc::SwerveDriveKinematicsConstraint<NumModules>, NumModules>;
py::class_<typename frc::SwerveDriveKinematicsConstraint<NumModules>, std::shared_ptr<typename frc::SwerveDriveKinematicsConstraint<NumModules>>, SwerveDriveKinematicsConstraint_Trampoline, TrajectoryConstraint> cls_SwerveDriveKinematicsConstraint;




    py::module &m;
    std::string clsName;

bind_frc__SwerveDriveKinematicsConstraint(py::module &m, const char * clsName) :
    cls_SwerveDriveKinematicsConstraint(m, clsName),



    m(m),
    clsName(clsName)
{}

void finish(const char * set_doc = NULL, const char * add_doc = NULL) {

    
  cls_SwerveDriveKinematicsConstraint.doc() =
    "A class that enforces constraints on the swerve drive kinematics.\n"
"This can be used to ensure that the trajectory is constructed so that the\n"
"commanded velocities of the wheels stay below a certain limit.";

  cls_SwerveDriveKinematicsConstraint
      .def(py::init<const frc::SwerveDriveKinematics<NumModules>&, units::meters_per_second_t>(),
      py::arg("kinematics"), py::arg("maxSpeed"), release_gil()    , py::keep_alive<1, 2>()
  )
    
      .def("maxVelocity", &frc::SwerveDriveKinematicsConstraint<NumModules>::MaxVelocity,
      py::arg("pose"), py::arg("curvature"), py::arg("velocity"), release_gil()
  )
    
      .def("minMaxAcceleration", &frc::SwerveDriveKinematicsConstraint<NumModules>::MinMaxAcceleration,
      py::arg("pose"), py::arg("curvature"), py::arg("speed"), release_gil()
  )
    
;

  

    if (set_doc) {
        cls_SwerveDriveKinematicsConstraint.doc() = set_doc;
    }
    if (add_doc) {
        cls_SwerveDriveKinematicsConstraint.doc() = py::cast<std::string>(cls_SwerveDriveKinematicsConstraint.doc()) + add_doc;
    }

    
}

}; // struct bind_frc__SwerveDriveKinematicsConstraint

}; // namespace rpygen