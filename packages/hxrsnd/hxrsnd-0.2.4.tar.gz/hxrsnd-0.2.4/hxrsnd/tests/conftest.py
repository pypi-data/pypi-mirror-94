import inspect
import logging
import math

import numpy as np
import pandas as pd
import pytest
from bluesky.tests.conftest import RE as fresh_RE  # noqa
from lmfit.models import LorentzianModel
from ophyd.areadetector.base import EpicsSignalWithRBV
from ophyd.device import Component as Cmp
from ophyd.device import Device
from ophyd.signal import Signal
from ophyd.sim import (FakeEpicsSignal, SynAxis, SynSignal, fake_device_cache,
                       make_fake_device)
from pcdsdevices.areadetector.detectors import PCDSAreaDetector

from ..sndmotor import CalibMotor

logger = logging.getLogger(__name__)

# Define the requires epics
try:
    import epics
    pv = epics.PV("XCS:USR:MMS:01")
    try:
        val = pv.get()
    except Exception:
        val = None
except Exception:
    val = None


epics_subnet = val is not None
requires_epics = pytest.mark.skipif(not epics_subnet,
                                    reason="Could not connect to sample PV")


# Enable the logging level to be set from the command line
def pytest_addoption(parser):
    parser.addoption("--log", action="store", default="INFO",
                     help="Set the level of the log")
    parser.addoption("--logfile", action="store", default=None,
                     help="Write the log output to specified file path")


class Diode(SynSignal):
    """
    Simulated Diode

    Evaluate a point on a Lorentz function based on the value of a motor

    By default, the amplitude and sigma values will create a max signal of 1.0,
    representing a normalized diode signal

    Parameters
    ----------
    name : str

    motor : obj

    motor_field : str
        Name of field to use as independent variable

    center : float
        Center position of Lorentz

    sigma : float, optional
        Width of distribution

    amplitude : float, optional
        Height of distribution

    noise_multiplier : float, optional
        Multipler for uniform noise of the diode. If left as None, no noise will
        be applied
    """
    def __init__(self, name, motor, motor_field, center,
                 sigma=1, amplitude=math.pi,
                 noise_multiplier=None, **kwargs):
        # Eliminate noise if not requested
        noise = noise_multiplier or 0.
        lorentz = LorentzianModel()

        def func():
            # Evaluate position in distribution
            m = motor.read()[motor_field]['value']
            v = lorentz.eval(x=np.array(m), amplitude=amplitude, sigma=sigma,
                             center=center)
            # Add uniform noise
            v += np.random.uniform(-1, 1) * noise
            return v

        # Instantiate Reader
        super().__init__(name=name, func=func, **kwargs)


class SynCentroid(SynSignal):
    """
    Synthetic centroid signal.
    """
    def __init__(self, motors, weights, noise_multiplier=None, name=None,
                 *args, **kwargs):
        # Eliminate noise if not requested
        self.motors = motors
        self.weights = weights
        self.noise = noise_multiplier or 0.

        def func():
            # Evaluate the positions of each motor
            pos = [m.position for m in self.motors] or [0, 0]
            # Get the centroid position
            cent = np.dot(pos, self.weights)
            # Add uniform noise
            cent += int(np.round(np.random.uniform(-1, 1) * self.noise))
            return cent

        # Instantiate the synsignal
        super().__init__(name=name, func=func, **kwargs)


class SynCamera(Device):
    """
    Simulated camera that has centroids as components.
    """
    centroid_x = Cmp(SynCentroid, motors=[], weights=[1, 0.25])
    centroid_y = Cmp(SynCentroid, motors=[], weights=[1, -0.25])

    def __init__(self, motor1, motor2, delay, name=None, *args, **kwargs):
        # Create the base class
        super().__init__("SYN:CAMERA", name=name, *args, **kwargs)

        # Define the centroid components using the inputted motors
        self.centroid_x.motors = [motor1, delay]
        self.centroid_y.motors = [motor2, delay]

        # Add them to _signals
        self._signals['centroid_x'] = self.centroid_x
        self._signals['centroid_y'] = self.centroid_y
        # Add them to the read_attrs
        self.read_attrs = ["centroid_x", "centroid_y"]

    def trigger(self):
        return self.centroid_x.trigger() & self.centroid_y.trigger()


class CalibTest(CalibMotor):
    motor = Cmp(SynAxis, name="test_axis")

    def __init__(self, *args, name="calib", m1=None, m2=None, **kwargs):
        super().__init__(*args, name="calib", **kwargs)
        self.calib_detector = SynCamera(m1, m2, self.motor, name="camera")
        self.calib_motors = [m1, m2]
        self.motor_fields = [self.motor.name]
        self.detector_fields = ['centroid_x', 'centroid_y']
        self.set = self.move
        for m in [self.motor] + self.calib_motors:
            m.move = m.set

    @property
    def position(self):
        return self.motor.position

    def move(self, position, *args, **kwargs):
        # Perform the calibration move
        status = self.motor.set(position, *args, *kwargs)
        if self.has_calib and self.use_calib:
            status = status & self._calib_compensate(position)
        return status


# Simulated Crystal motor that goes where you tell it
crystal = SynAxis(name='angle')
m1 = SynAxis(name="m1")
m2 = SynAxis(name="m2")
delay = SynAxis(name="delay")


# Create a fixture to automatically instantiate logging setup
@pytest.fixture(scope='session', autouse=True)
def set_level(pytestconfig):
    # Read user input logging level
    log_level = getattr(logging, pytestconfig.getoption('--log'), None)

    # Report invalid logging level
    if not isinstance(log_level, int):
        raise ValueError("Invalid log level : {}".format(log_level))

    # Create basic configuration
    logging.basicConfig(level=log_level,
                        filename=pytestconfig.getoption('--logfile'))


@pytest.fixture(scope='function')
def get_calib_motor(request):
    m1 = SynAxis(name="m1")
    m2 = SynAxis(name="m2")
    return CalibTest("test", m1=m1, m2=m2)


def get_classes_in_module(module, subcls=None, blacklist=None):
    classes = []
    blacklist = blacklist or list()
    all_classes = [cls for _, cls in inspect.getmembers(module)
                   if cls not in blacklist]
    for cls in all_classes:
        try:
            if cls.__module__ == module.__name__:
                if subcls is not None:
                    try:
                        if not issubclass(cls, subcls):
                            continue
                    except TypeError:
                        continue
                classes.append(cls)
        except AttributeError:
            pass
    return classes


# Create a fake epics device
def fake_device(device, name="TEST"):
    device = make_fake_device(device)
    return device(name, name=name)


def fake_detector(detector, name="TEST"):
    """Set the plugin_type signal to be _plugin_type for all plugins."""
    def change_all_plugin_types(comp):
        if hasattr(comp, "component_names"):
            if hasattr(comp, "_plugin_type"):
                comp.plugin_type = Cmp(Signal, value=comp._plugin_type)
            else:
                for name in comp.component_names:
                    sub_comp = getattr(comp, name)
                    if type(sub_comp) is Cmp:
                        sub_comp = change_all_plugin_types(sub_comp.cls)
        return comp
    detector = change_all_plugin_types(detector)
    detector = make_fake_device(detector)
    return detector(name, name=name)


# Hotfix area detector plugins for tests
for comp in (PCDSAreaDetector.image1, PCDSAreaDetector.stats2):
    plugin_class = comp.cls
    plugin_class.plugin_type = Cmp(Signal, value=plugin_class._plugin_type)

# Hotfix make_fake_device for ophyd=1.2.0
fake_device_cache[EpicsSignalWithRBV] = FakeEpicsSignal

test_df_scan = pd.DataFrame(
    [[-1, 0, 0, -0.25, 0.25],
     [-0.5, 0, 0, -0.125, 0.125],
     [0, 0, 0, 0, 0],
     [0.5, 0, 0, 0.125, -0.125],
     [1, 0, 0, 0.25, -0.25]
     ],
    index=np.linspace(-1, 1, 5),
    columns=["delay", "m1_pre", "m2_pre", "camera_centroid_x",
             "camera_centroid_y"]
)
