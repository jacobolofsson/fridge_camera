from unittest.mock import MagicMock, patch

import pytest

MIN_VAL = 12100
MAX_VAL = 12730


@pytest.fixture()
def sensor():
    with patch.dict(
        "sys.modules",
        {
            "board": MagicMock(),
            "busio": MagicMock(),
            "adafruit_ads1x15": MagicMock(),
            "adafruit_ads1x15.ads1115": MagicMock(),
            "adafruit_ads1x15.analog_in": MagicMock(),
        }
    ):
        from fridgecamera.sensor import Sensor
        yield Sensor(MIN_VAL, MAX_VAL)


@pytest.mark.parametrize(("analog_val", "expected_angle"), [
    (MIN_VAL, 0),
    (MAX_VAL, 90),
    (MIN_VAL + (MAX_VAL-MIN_VAL)/2, 45),
])
def test_read_angle(sensor, analog_val, expected_angle) -> None:
    from adafruit_ads1x15.analog_in import AnalogIn
    AnalogIn.return_value.value = analog_val
    assert pytest.approx(sensor.readAngle()) == expected_angle
