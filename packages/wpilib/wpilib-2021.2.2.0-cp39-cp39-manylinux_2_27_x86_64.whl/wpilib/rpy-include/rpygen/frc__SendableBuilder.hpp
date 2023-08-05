
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <../_impl/include/frc/smartdashboard/SendableBuilder.h>






namespace rpygen {

using namespace frc;


template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
struct Pyfrc__SendableBuilder : PyTrampolineBase {
    using PyTrampolineBase::PyTrampolineBase;



#ifndef RPYGEN_DISABLE_SetSmartDashboardType_KRTTwine
    void SetSmartDashboardType(const wpi::Twine& type) override {
RPYBUILD_OVERRIDE_PURE_NAME(SendableBuilder,PYBIND11_TYPE(void), CxxBase, "setSmartDashboardType", SetSmartDashboardType,type);    }
#endif

#ifndef RPYGEN_DISABLE_SetActuator_b
    void SetActuator(bool value) override {
RPYBUILD_OVERRIDE_PURE_NAME(SendableBuilder,PYBIND11_TYPE(void), CxxBase, "setActuator", SetActuator,value);    }
#endif

#ifndef RPYGEN_DISABLE_SetSafeState_Tfunction_void___
    void SetSafeState(std::function<void ( )> func) override {
RPYBUILD_OVERRIDE_PURE_NAME(SendableBuilder,PYBIND11_TYPE(void), CxxBase, "setSafeState", SetSafeState,func);    }
#endif

#ifndef RPYGEN_DISABLE_SetUpdateTable_Tfunction_void___
    void SetUpdateTable(std::function<void ( )> func) override {
RPYBUILD_OVERRIDE_PURE_NAME(SendableBuilder,PYBIND11_TYPE(void), CxxBase, "setUpdateTable", SetUpdateTable,func);    }
#endif

#ifndef RPYGEN_DISABLE_GetEntry_KRTTwine
    nt::NetworkTableEntry GetEntry(const wpi::Twine& key) override {
RPYBUILD_OVERRIDE_PURE_NAME(SendableBuilder,PYBIND11_TYPE(nt::NetworkTableEntry), CxxBase, "getEntry", GetEntry,key);    }
#endif

#ifndef RPYGEN_DISABLE_AddBooleanProperty_KRTTwine_Tfunction_bool____Tfunction_void_bool__
    void AddBooleanProperty(const wpi::Twine& key, std::function<bool ( )> getter, std::function<void ( bool )> setter) override {
RPYBUILD_OVERRIDE_PURE_NAME(SendableBuilder,PYBIND11_TYPE(void), CxxBase, "addBooleanProperty", AddBooleanProperty,key, getter, setter);    }
#endif

#ifndef RPYGEN_DISABLE_AddDoubleProperty_KRTTwine_Tfunction_double____Tfunction_void_double__
    void AddDoubleProperty(const wpi::Twine& key, std::function<double ( )> getter, std::function<void ( double )> setter) override {
RPYBUILD_OVERRIDE_PURE_NAME(SendableBuilder,PYBIND11_TYPE(void), CxxBase, "addDoubleProperty", AddDoubleProperty,key, getter, setter);    }
#endif

#ifndef RPYGEN_DISABLE_AddStringProperty_KRTTwine_Tstring____TStringRef__
    void AddStringProperty(const wpi::Twine& key, std::function<std::string ( )> getter, std::function<void ( wpi::StringRef )> setter) override {
RPYBUILD_OVERRIDE_PURE_NAME(SendableBuilder,PYBIND11_TYPE(void), CxxBase, "addStringProperty", AddStringProperty,key, getter, setter);    }
#endif

#ifndef RPYGEN_DISABLE_AddBooleanArrayProperty_KRTTwine_Tvector_int_____TArrayRef_int___
    void AddBooleanArrayProperty(const wpi::Twine& key, std::function<std::vector<int> ( )> getter, std::function<void ( wpi::ArrayRef<int> )> setter) override {
RPYBUILD_OVERRIDE_PURE_NAME(SendableBuilder,PYBIND11_TYPE(void), CxxBase, "addBooleanArrayProperty", AddBooleanArrayProperty,key, getter, setter);    }
#endif

#ifndef RPYGEN_DISABLE_AddDoubleArrayProperty_KRTTwine_Tvector_double_____TArrayRef_double___
    void AddDoubleArrayProperty(const wpi::Twine& key, std::function<std::vector<double> ( )> getter, std::function<void ( wpi::ArrayRef<double> )> setter) override {
RPYBUILD_OVERRIDE_PURE_NAME(SendableBuilder,PYBIND11_TYPE(void), CxxBase, "addDoubleArrayProperty", AddDoubleArrayProperty,key, getter, setter);    }
#endif

#ifndef RPYGEN_DISABLE_AddStringArrayProperty_KRTTwine_Tstring_____Tstring___
    void AddStringArrayProperty(const wpi::Twine& key, std::function<std::vector<std::string> ( )> getter, std::function<void ( wpi::ArrayRef<std::string> )> setter) override {
RPYBUILD_OVERRIDE_PURE_NAME(SendableBuilder,PYBIND11_TYPE(void), CxxBase, "addStringArrayProperty", AddStringArrayProperty,key, getter, setter);    }
#endif

#ifndef RPYGEN_DISABLE_AddRawProperty_KRTTwine_Tstring____TStringRef__
    void AddRawProperty(const wpi::Twine& key, std::function<std::string ( )> getter, std::function<void ( wpi::StringRef )> setter) override {
RPYBUILD_OVERRIDE_PURE_NAME(SendableBuilder,PYBIND11_TYPE(void), CxxBase, "addRawProperty", AddRawProperty,key, getter, setter);    }
#endif

#ifndef RPYGEN_DISABLE_AddValueProperty_KRTTwine_TValue_____TValue___
    void AddValueProperty(const wpi::Twine& key, std::function<std::shared_ptr<nt::Value> ( )> getter, std::function<void ( std::shared_ptr<nt::Value> )> setter) override {
RPYBUILD_OVERRIDE_PURE_NAME(SendableBuilder,PYBIND11_TYPE(void), CxxBase, "addValueProperty", AddValueProperty,key, getter, setter);    }
#endif

#ifndef RPYGEN_DISABLE_AddSmallStringProperty_KRTTwine_TSmallVectorImpl_char__buf___TStringRef__
    void AddSmallStringProperty(const wpi::Twine& key, std::function<wpi::StringRef ( wpi::SmallVectorImpl<char> & buf )> getter, std::function<void ( wpi::StringRef )> setter) override {
RPYBUILD_OVERRIDE_PURE_NAME(SendableBuilder,PYBIND11_TYPE(void), CxxBase, "addSmallStringProperty", AddSmallStringProperty,key, getter, setter);    }
#endif

#ifndef RPYGEN_DISABLE_AddSmallBooleanArrayProperty_KRTTwine_TSmallVectorImpl_int__buf___TArrayRef_int___
    void AddSmallBooleanArrayProperty(const wpi::Twine& key, std::function<wpi::ArrayRef<int> ( wpi::SmallVectorImpl<int> & buf )> getter, std::function<void ( wpi::ArrayRef<int> )> setter) override {
RPYBUILD_OVERRIDE_PURE_NAME(SendableBuilder,PYBIND11_TYPE(void), CxxBase, "addSmallBooleanArrayProperty", AddSmallBooleanArrayProperty,key, getter, setter);    }
#endif

#ifndef RPYGEN_DISABLE_AddSmallDoubleArrayProperty_KRTTwine_TSmallVectorImpl_double__buf___TArrayRef_double___
    void AddSmallDoubleArrayProperty(const wpi::Twine& key, std::function<wpi::ArrayRef<double> ( wpi::SmallVectorImpl<double> & buf )> getter, std::function<void ( wpi::ArrayRef<double> )> setter) override {
RPYBUILD_OVERRIDE_PURE_NAME(SendableBuilder,PYBIND11_TYPE(void), CxxBase, "addSmallDoubleArrayProperty", AddSmallDoubleArrayProperty,key, getter, setter);    }
#endif

#ifndef RPYGEN_DISABLE_AddSmallStringArrayProperty_KRTTwine_Tstring__buf___Tstring___
    void AddSmallStringArrayProperty(const wpi::Twine& key, std::function<wpi::ArrayRef<std::string> ( wpi::SmallVectorImpl<std::string> & buf )> getter, std::function<void ( wpi::ArrayRef<std::string> )> setter) override {
RPYBUILD_OVERRIDE_PURE_NAME(SendableBuilder,PYBIND11_TYPE(void), CxxBase, "addSmallStringArrayProperty", AddSmallStringArrayProperty,key, getter, setter);    }
#endif

#ifndef RPYGEN_DISABLE_AddSmallRawProperty_KRTTwine_TSmallVectorImpl_char__buf___TStringRef__
    void AddSmallRawProperty(const wpi::Twine& key, std::function<wpi::StringRef ( wpi::SmallVectorImpl<char> & buf )> getter, std::function<void ( wpi::StringRef )> setter) override {
RPYBUILD_OVERRIDE_PURE_NAME(SendableBuilder,PYBIND11_TYPE(void), CxxBase, "addSmallRawProperty", AddSmallRawProperty,key, getter, setter);    }
#endif

#ifndef RPYGEN_DISABLE_GetTable_v
    std::shared_ptr<nt::NetworkTable > GetTable() override {
RPYBUILD_OVERRIDE_PURE_NAME(SendableBuilder,PYBIND11_TYPE(std::shared_ptr<nt::NetworkTable >), CxxBase, "getTable", GetTable,);    }
#endif




};

}; // namespace rpygen
