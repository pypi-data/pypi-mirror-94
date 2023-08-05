from . import _init_simulation

# needed for dcmotor return value, TODO fix in robotpy-build
from wpimath._controls._controls import plant as _

# autogenerated by 'robotpy-build create-imports wpilib.simulation'
from ._simulation import (
    ADXRS450_GyroSim,
    AddressableLEDSim,
    AnalogEncoderSim,
    AnalogGyroSim,
    AnalogInputSim,
    AnalogOutputSim,
    AnalogTriggerSim,
    BatterySim,
    BuiltInAccelerometerSim,
    CallbackStore,
    DIOSim,
    DifferentialDrivetrainSim,
    DigitalPWMSim,
    DriverStationSim,
    DutyCycleEncoderSim,
    DutyCycleSim,
    ElevatorSim,
    EncoderSim,
    FlywheelSim,
    GenericHIDSim,
    JoystickSim,
    LinearSystemSim_1_1_1,
    LinearSystemSim_1_1_2,
    LinearSystemSim_2_1_1,
    LinearSystemSim_2_1_2,
    LinearSystemSim_2_2_1,
    LinearSystemSim_2_2_2,
    Mechanism2D,
    PCMSim,
    PDPSim,
    PWMSim,
    RelaySim,
    RoboRioSim,
    SPIAccelerometerSim,
    SimDeviceSim,
    SingleJointedArmSim,
    XboxControllerSim,
    getProgramStarted,
    isTimingPaused,
    pauseTiming,
    restartTiming,
    resumeTiming,
    setProgramStarted,
    setRuntimeType,
    stepTiming,
    stepTimingAsync,
    waitForProgramStart,
)

__all__ = [
    "ADXRS450_GyroSim",
    "AddressableLEDSim",
    "AnalogEncoderSim",
    "AnalogGyroSim",
    "AnalogInputSim",
    "AnalogOutputSim",
    "AnalogTriggerSim",
    "BatterySim",
    "BuiltInAccelerometerSim",
    "CallbackStore",
    "DIOSim",
    "DifferentialDrivetrainSim",
    "DigitalPWMSim",
    "DriverStationSim",
    "DutyCycleEncoderSim",
    "DutyCycleSim",
    "ElevatorSim",
    "EncoderSim",
    "FlywheelSim",
    "GenericHIDSim",
    "JoystickSim",
    "LinearSystemSim_1_1_1",
    "LinearSystemSim_1_1_2",
    "LinearSystemSim_2_1_1",
    "LinearSystemSim_2_1_2",
    "LinearSystemSim_2_2_1",
    "LinearSystemSim_2_2_2",
    "Mechanism2D",
    "PCMSim",
    "PDPSim",
    "PWMSim",
    "RelaySim",
    "RoboRioSim",
    "SPIAccelerometerSim",
    "SimDeviceSim",
    "SingleJointedArmSim",
    "XboxControllerSim",
    "getProgramStarted",
    "isTimingPaused",
    "pauseTiming",
    "restartTiming",
    "resumeTiming",
    "setProgramStarted",
    "setRuntimeType",
    "stepTiming",
    "stepTimingAsync",
    "waitForProgramStart",
]
