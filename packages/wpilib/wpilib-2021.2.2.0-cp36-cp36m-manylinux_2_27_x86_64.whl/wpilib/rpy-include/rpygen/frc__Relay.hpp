
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <../_impl/include/frc/Relay.h>

#include <frc/smartdashboard/SendableBuilder.h>
#include <wpi/SmallString.h>




#include <rpygen/frc__MotorSafety.hpp>
#include <rpygen/frc__Sendable.hpp>

namespace rpygen {

using namespace frc;


template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
using PyBasefrc__Relay = 
    Pyfrc__MotorSafety<
    Pyfrc__Sendable<
        PyTrampolineBase
    
    , CxxBase
    >
    
    , CxxBase
    >
;

template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
struct Pyfrc__Relay : PyBasefrc__Relay<PyTrampolineBase, CxxBase> {
    using PyBasefrc__Relay<PyTrampolineBase, CxxBase>::PyBasefrc__Relay;



#ifndef RPYGEN_DISABLE_StopMotor_v
    void StopMotor() override {
PYBIND11_OVERRIDE_NAME(PYBIND11_TYPE(void), CxxBase, "stopMotor", StopMotor,);    }
#endif

#ifndef RPYGEN_DISABLE_KGetDescription_RTraw_ostream
    void GetDescription(wpi::raw_ostream& desc) const override {
        auto custom_fn = [&](py::function &overload) {
  desc << py::cast<std::string>(overload());
}
;
RPYBUILD_OVERRIDE_CUSTOM_NAME(PYBIND11_TYPE(void), CxxBase, "getDescription", GetDescription,desc);    }
#endif

#ifndef RPYGEN_DISABLE_InitSendable_RTSendableBuilder
    void InitSendable(frc::SendableBuilder& builder) override {
PYBIND11_OVERRIDE_NAME(PYBIND11_TYPE(void), CxxBase, "initSendable", InitSendable,builder);    }
#endif




};

}; // namespace rpygen
