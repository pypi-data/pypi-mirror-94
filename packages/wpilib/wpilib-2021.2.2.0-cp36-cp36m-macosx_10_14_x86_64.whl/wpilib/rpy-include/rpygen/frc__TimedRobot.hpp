
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <../_impl/include/frc/TimedRobot.h>





#include <rpygen/frc__IterativeRobotBase.hpp>

namespace rpygen {

using namespace frc;


template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
using PyBasefrc__TimedRobot = 
    Pyfrc__IterativeRobotBase<
        PyTrampolineBase
    
    , CxxBase
    >
;

template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
struct Pyfrc__TimedRobot : PyBasefrc__TimedRobot<PyTrampolineBase, CxxBase> {
    using PyBasefrc__TimedRobot<PyTrampolineBase, CxxBase>::PyBasefrc__TimedRobot;



#ifndef RPYGEN_DISABLE_StartCompetition_v
    void StartCompetition() override {
PYBIND11_OVERRIDE_NAME(PYBIND11_TYPE(void), CxxBase, "startCompetition", StartCompetition,);    }
#endif

#ifndef RPYGEN_DISABLE_EndCompetition_v
    void EndCompetition() override {
PYBIND11_OVERRIDE_NAME(PYBIND11_TYPE(void), CxxBase, "endCompetition", EndCompetition,);    }
#endif




};

}; // namespace rpygen
