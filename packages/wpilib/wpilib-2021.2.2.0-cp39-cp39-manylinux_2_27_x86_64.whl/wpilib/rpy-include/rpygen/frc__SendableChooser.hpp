
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <../_impl/include/frc/smartdashboard/SendableChooser.h>





#include <rpygen/frc__SendableChooserBase.hpp>

namespace rpygen {

using namespace frc;


template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
using PyBasefrc__SendableChooser = 
    Pyfrc__SendableChooserBase<
        PyTrampolineBase
    
    , CxxBase
    >
;

template <typename PyTrampolineBase, typename T, typename CxxBase = PyTrampolineBase>
struct Pyfrc__SendableChooser : PyBasefrc__SendableChooser<PyTrampolineBase, CxxBase> {
    using PyBasefrc__SendableChooser<PyTrampolineBase, CxxBase>::PyBasefrc__SendableChooser;



#ifndef RPYGEN_DISABLE_InitSendable_RTSendableBuilder
    void InitSendable(SendableBuilder& builder) override {
PYBIND11_OVERRIDE_NAME(PYBIND11_TYPE(void), CxxBase, "initSendable", InitSendable,builder);    }
#endif




};

}; // namespace rpygen


namespace rpygen {

using namespace frc;


template <typename T>
struct bind_frc__SendableChooser {

    

      using SendableChooser_Trampoline = rpygen::Pyfrc__SendableChooser<typename frc::SendableChooser<T>, T>;
py::class_<typename frc::SendableChooser<T>, std::shared_ptr<typename frc::SendableChooser<T>>, SendableChooser_Trampoline, SendableChooserBase> cls_SendableChooser;




    py::module &m;
    std::string clsName;

bind_frc__SendableChooser(py::module &m, const char * clsName) :
    cls_SendableChooser(m, clsName),



    m(m),
    clsName(clsName)
{}

void finish(const char * set_doc = NULL, const char * add_doc = NULL) {

    
  cls_SendableChooser.doc() =
    "The SendableChooser class is a useful tool for presenting a selection of\n"
"options to the SmartDashboard.\n"
"\n"
"For instance, you may wish to be able to select between multiple autonomous\n"
"modes. You can do this by putting every possible Command you want to run as\n"
"an autonomous into a SendableChooser and then put it into the SmartDashboard\n"
"to have a list of options appear on the laptop. Once autonomous starts,\n"
"simply ask the SendableChooser what the selected value is.\n"
"\n"
"@tparam T The type of values to be stored\n"
"@see SmartDashboard";

  cls_SendableChooser
      .def(py::init<>(), release_gil()
  )
    
      .def("addOption", &frc::SendableChooser<T>::AddOption,
      py::arg("name"), py::arg("object"), release_gil(), py::doc(
    "Adds the given object to the list of options.\n"
"\n"
"On the SmartDashboard on the desktop, the object will appear as the given\n"
"name.\n"
"\n"
":param name:   the name of the option\n"
":param object: the option")
  )
    
      .def("setDefaultOption", &frc::SendableChooser<T>::SetDefaultOption,
      py::arg("name"), py::arg("object"), release_gil(), py::doc(
    "Add the given object to the list of options and marks it as the default.\n"
"\n"
"Functionally, this is very close to AddOption() except that it will use\n"
"this as the default option if none other is explicitly selected.\n"
"\n"
":param name:   the name of the option\n"
":param object: the option")
  )
    
      .def("getSelected", [](frc::SendableChooser<T> * __that) {
  return __that->GetSelected();
}
, py::doc(
    "Returns a copy of the selected option (a raw pointer U* if T =\n"
"std::unique_ptr<U> or a std::weak_ptr<U> if T = std::shared_ptr<U>).\n"
"\n"
"If there is none selected, it will return the default. If there is none\n"
"selected and no default, then it will return a value-initialized instance.\n"
"For integer types, this is 0. For container types like std::string, this is\n"
"an empty string.\n"
"\n"
":returns: The option selected")
  )
    
      .def("initSendable", &frc::SendableChooser<T>::InitSendable,
      py::arg("builder"), release_gil()
  )
    
;

  

    if (set_doc) {
        cls_SendableChooser.doc() = set_doc;
    }
    if (add_doc) {
        cls_SendableChooser.doc() = py::cast<std::string>(cls_SendableChooser.doc()) + add_doc;
    }

    
}

}; // struct bind_frc__SendableChooser

}; // namespace rpygen