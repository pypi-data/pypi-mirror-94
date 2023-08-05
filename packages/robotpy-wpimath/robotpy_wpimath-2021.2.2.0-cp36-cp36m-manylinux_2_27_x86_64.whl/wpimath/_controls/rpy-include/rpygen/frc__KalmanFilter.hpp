
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <../../_impl/include/frc/estimator/KalmanFilter.h>





namespace rpygen {

using namespace frc;


template <int States, int Inputs, int Outputs>
struct bind_frc__KalmanFilter {

    

    py::class_<typename frc::KalmanFilter<States, Inputs, Outputs>, std::shared_ptr<typename frc::KalmanFilter<States, Inputs, Outputs>>> cls_KalmanFilter;




    py::module &m;
    std::string clsName;

bind_frc__KalmanFilter(py::module &m, const char * clsName) :
    cls_KalmanFilter(m, clsName),



    m(m),
    clsName(clsName)
{}

void finish(const char * set_doc = NULL, const char * add_doc = NULL) {

    
  

  cls_KalmanFilter
      .def(py::init<LinearSystem<States, Inputs, Outputs>&, const wpi::array<double, States>&, const wpi::array<double, Outputs>&, units::second_t>(),
      py::arg("plant"), py::arg("stateStdDevs"), py::arg("measurementStdDevs"), py::arg("dt"), release_gil()    , py::keep_alive<1, 2>()    , py::keep_alive<1, 3>()    , py::keep_alive<1, 4>(), py::doc(
    "Constructs a state-space observer with the given plant.\n"
"\n"
":param plant:              The plant used for the prediction step.\n"
":param stateStdDevs:       Standard deviations of model states.\n"
":param measurementStdDevs: Standard deviations of measurements.\n"
":param dt:                 Nominal discretization timestep.")
  )
    
;

  

    if (set_doc) {
        cls_KalmanFilter.doc() = set_doc;
    }
    if (add_doc) {
        cls_KalmanFilter.doc() = py::cast<std::string>(cls_KalmanFilter.doc()) + add_doc;
    }

    
}

}; // struct bind_frc__KalmanFilter

}; // namespace rpygen