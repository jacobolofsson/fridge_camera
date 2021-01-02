from unittest.mock import MagicMock, patch

from fridgecamera.fridge import Image


def test_filename() -> None:
    mock_image = MagicMock()
    mock_angle = MagicMock()
    test_timestamp = "1111-22-33"
    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value.strftime.return_value = test_timestamp
        img = Image(mock_image, mock_angle)
        assert img.getFilename() == f"fridge_{test_timestamp}.png"


def test_attrs() -> None:
    mock_image = MagicMock()
    mock_angle = MagicMock()
    img = Image(mock_image, mock_angle)
    assert img.image is mock_image
    assert img.doorAngle is mock_angle
