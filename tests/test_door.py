from unittest.mock import MagicMock

import pytest

from fridgecamera.fridge import Door


def test_update_angle():
    mock_sensor = MagicMock()
    door = Door(mock_sensor)
    assert door.angle == 0.0
    door.updateAngle()
    assert door.angle is mock_sensor.readAngle.return_value


@pytest.mark.parametrize(("angle", "is_closed"), [
    (0, False),
    (5, False),
    (55, False),
    (60, True),
    (85, True),
    (90, True),
])
def test_closed_door(angle, is_closed):
    mock_sensor = MagicMock()
    mock_sensor.readAngle.return_value = angle
    door = Door(mock_sensor)
    door.updateAngle()
    assert door.isClosed() == is_closed


@pytest.mark.parametrize(("angle", "in_view"), [
    (0, False),
    (1, True),
    (5, True),
    (9, True),
    (10, False),
    (55, False),
    (85, False),
    (90, False),
])
def test_in_view(angle, in_view):
    mock_sensor = MagicMock()
    mock_sensor.readAngle.return_value = angle
    door = Door(mock_sensor)
    door.updateAngle()
    assert door.isInView() == in_view
