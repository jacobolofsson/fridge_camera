import logging

import board
import busio
from adafruit_ads1x15.ads1115 import ADS1115, P0
from adafruit_ads1x15.analog_in import AnalogIn

MAX_ANGLE = 90


class Sensor():
    def __init__(self, min_sensor_val: int, max_sensor_val: int) -> None:
        self._min_sensor_val = min_sensor_val
        self._max_sensor_val = max_sensor_val
        self._max_angle = MAX_ANGLE

        self.logger = logging.getLogger(__name__)
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = ADS1115(i2c)

    def readAngle(self) -> float:
        chan = AnalogIn(self.sensor, P0)
        angle = self._valueToAngle(chan.value)
        self.logger.debug(f"Angle: {angle} Value: {chan.value}")
        return angle

    def _valueToAngle(self, value: int) -> float:
        shifted = (value - self._min_sensor_val)
        normalized = shifted / (self._max_sensor_val - self._min_sensor_val)
        return normalized * self._max_angle
