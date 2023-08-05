
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <..\_impl\include\frc\MotorSafety.h>

#include <wpi/SmallString.h>




#include <rpygen/frc__ErrorBase.hpp>

namespace rpygen {

using namespace frc;


template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
using PyBasefrc__MotorSafety = 
    Pyfrc__ErrorBase<
        PyTrampolineBase
    
    , CxxBase
    >
;

template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
struct Pyfrc__MotorSafety : PyBasefrc__MotorSafety<PyTrampolineBase, CxxBase> {
    using PyBasefrc__MotorSafety<PyTrampolineBase, CxxBase>::PyBasefrc__MotorSafety;



#ifndef RPYGEN_DISABLE_StopMotor_v
    void StopMotor() override {
RPYBUILD_OVERRIDE_PURE_NAME(MotorSafety,PYBIND11_TYPE(void), CxxBase, "stopMotor", StopMotor,);    }
#endif

#ifndef RPYGEN_DISABLE_KGetDescription_RTraw_ostream
    void GetDescription(wpi::raw_ostream& desc) const override {
        auto custom_fn = [&](py::function &overload) {
  desc << py::cast<std::string>(overload());
}
;
        RPYBUILD_OVERRIDE_PURE_CUSTOM_NAME(MotorSafety,PYBIND11_TYPE(void), CxxBase, "getDescription", GetDescription,desc);    }
#endif




};

}; // namespace rpygen
