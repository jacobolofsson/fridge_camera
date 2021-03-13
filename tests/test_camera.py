from pathlib import Path
from typing import Iterable
from unittest.mock import MagicMock, patch

import pytest

from fridgecamera.fridge import Camera

TEST_CAM_ID = 999
TEST_PATH = Path("this/path/does/not/exist")


def test_cam_id() -> None:
    with patch("cv2.VideoCapture") as mock_camera:
        Camera(TEST_CAM_ID, TEST_PATH)
    mock_camera.assert_called_once_with(TEST_CAM_ID)


@pytest.fixture()
def camera(tmp_path) -> Iterable[Camera]:
    with patch("cv2.VideoCapture") as mock_camera:
        mock_camera.return_value.read.return_value = (MagicMock(), MagicMock())
        yield Camera(TEST_CAM_ID, tmp_path)


def test_unstored_picture(camera: Camera) -> None:
    camera.takePicture(999)
    assert camera.hasUnstoredPicture()


def test_no_unstored_picture(camera: Camera) -> None:
    assert not camera.hasUnstoredPicture()


def test_take_picture(camera: Camera) -> None:
    test_angle = 999
    with patch("fridgecamera.fridge.Image") as mock_img:
        camera.takePicture(test_angle)

    camera.camera.read.assert_called_once_with()
    _, frame = camera.camera.read.return_value
    mock_img.assert_called_once_with(frame, test_angle)


def test_store_picture(camera: Camera, tmp_path: Path) -> None:
    mock_filename = "test_filename.jpg"

    with patch("fridgecamera.fridge.Image") as mock_img:
        camera.takePicture(999)

    mock_img.return_value.getFilename.return_value = mock_filename

    with patch("cv2.imwrite") as mock_imwrite:
        filename = camera.storePictureAsFile()

    mock_imwrite.assert_called_once_with(
        f"{tmp_path}/{mock_filename}", mock_img.return_value.image,
    )

    assert filename == tmp_path / mock_filename
    assert not camera.hasUnstoredPicture()
