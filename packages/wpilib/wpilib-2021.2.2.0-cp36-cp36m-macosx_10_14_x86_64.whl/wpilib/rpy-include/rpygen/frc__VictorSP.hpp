
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <../_impl/include/frc/VictorSP.h>

#include <frc/smartdashboard/SendableBuilder.h>




#include <rpygen/frc__PWMSpeedController.hpp>

namespace rpygen {

using namespace frc;


template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
using PyBasefrc__VictorSP = 
    Pyfrc__PWMSpeedController<
        PyTrampolineBase
    
    , CxxBase
    >
;

template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
struct Pyfrc__VictorSP : PyBasefrc__VictorSP<PyTrampolineBase, CxxBase> {
    using PyBasefrc__VictorSP<PyTrampolineBase, CxxBase>::PyBasefrc__VictorSP;






};

}; // namespace rpygen
