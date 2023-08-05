
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <..\_impl\include\frc\AnalogOutput.h>

#include <frc/smartdashboard/SendableBuilder.h>




#include <rpygen/frc__ErrorBase.hpp>
#include <rpygen/frc__Sendable.hpp>

namespace rpygen {

using namespace frc;


template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
using PyBasefrc__AnalogOutput = 
    Pyfrc__ErrorBase<
    Pyfrc__Sendable<
        PyTrampolineBase
    
    , CxxBase
    >
    
    , CxxBase
    >
;

template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
struct Pyfrc__AnalogOutput : PyBasefrc__AnalogOutput<PyTrampolineBase, CxxBase> {
    using PyBasefrc__AnalogOutput<PyTrampolineBase, CxxBase>::PyBasefrc__AnalogOutput;



#ifndef RPYGEN_DISABLE_InitSendable_RTSendableBuilder
    void InitSendable(frc::SendableBuilder& builder) override {
PYBIND11_OVERRIDE_NAME(PYBIND11_TYPE(void), CxxBase, "initSendable", InitSendable,builder);    }
#endif



    using frc::AnalogOutput::m_channel;

};

}; // namespace rpygen
