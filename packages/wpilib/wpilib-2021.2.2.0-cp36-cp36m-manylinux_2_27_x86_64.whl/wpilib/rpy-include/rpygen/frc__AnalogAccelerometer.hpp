
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <../_impl/include/frc/AnalogAccelerometer.h>

#include <frc/smartdashboard/SendableBuilder.h>




#include <rpygen/frc__ErrorBase.hpp>
#include <rpygen/frc__PIDSource.hpp>
#include <rpygen/frc__Sendable.hpp>

namespace rpygen {

using namespace frc;


template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
using PyBasefrc__AnalogAccelerometer = 
    Pyfrc__ErrorBase<
    Pyfrc__PIDSource<
    Pyfrc__Sendable<
        PyTrampolineBase
    
    , CxxBase
    >
    
    , CxxBase
    >
    
    , CxxBase
    >
;

template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
struct Pyfrc__AnalogAccelerometer : PyBasefrc__AnalogAccelerometer<PyTrampolineBase, CxxBase> {
    using PyBasefrc__AnalogAccelerometer<PyTrampolineBase, CxxBase>::PyBasefrc__AnalogAccelerometer;



#ifndef RPYGEN_DISABLE_PIDGet_v
    double PIDGet() override {
PYBIND11_OVERRIDE_NAME(PYBIND11_TYPE(double), CxxBase, "pidGet", PIDGet,);    }
#endif

#ifndef RPYGEN_DISABLE_InitSendable_RTSendableBuilder
    void InitSendable(frc::SendableBuilder& builder) override {
PYBIND11_OVERRIDE_NAME(PYBIND11_TYPE(void), CxxBase, "initSendable", InitSendable,builder);    }
#endif




};

}; // namespace rpygen
