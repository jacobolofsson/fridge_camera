import logging

import adafruit_ads1x15.ads1115 as ADS
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn

MAX_ANGLE = 90
MAX_SENSOR_VAL = 12730
MIN_SENSOR_VAL = 12100


def valueToAngle(value: int) -> float:
    return (value - MIN_SENSOR_VAL) * MAX_ANGLE / \
        (MAX_SENSOR_VAL - MIN_SENSOR_VAL)


class Sensor():
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = ADS.ADS1115(i2c)

    def readAngle(self) -> float:
        chan = AnalogIn(self.sensor, ADS.P0)
        angle = valueToAngle(chan.value)
        self.logger.debug("Angle: ", angle, "Value:", chan.value)
        return angle
