from typing import Iterable
from unittest.mock import patch

import pytest

from fridgecamera.worker import Worker


@pytest.fixture(autouse=True)
def mock_time() -> Iterable[None]:
    with patch("time.sleep"):
        yield


@patch("fridgecamera.worker.Camera")
@patch("fridgecamera.worker.Door")
@patch("fridgecamera.worker.Sensor")
@patch("fridgecamera.worker.Uploader")
def test_worker(
    mock_uploader,
    mock_sensor,
    mock_door,
    mock_camera,
    tmp_path,
) -> None:
    test_id = 99
    test_path = tmp_path
    sensor_config = (12100, 12730)
    ftp_details = {
        "host": "testhost",
        "user": "testuser",
        "pass": "testpass",
        "path": "testpath"
    }
    fps = 1000
    Worker(test_id, test_path, sensor_config, ftp_details, fps)
    mock_uploader.assert_called_once_with(*ftp_details.values())
    mock_sensor.assert_called_once_with(*sensor_config)
    mock_door.assert_called_once_with(mock_sensor.return_value)
    mock_camera.assert_called_once_with(test_id, test_path)


@pytest.fixture()
@patch("fridgecamera.worker.Camera")
@patch("fridgecamera.worker.Door")
@patch("fridgecamera.worker.Sensor")
@patch("fridgecamera.worker.Uploader")
def worker(
    mock_uploader,
    mock_sensor,
    mock_door,
    mock_camera,
    tmp_path,
) -> Worker:
    return Worker(
        0,
        tmp_path,
        (0, 1),
        {
            "host": "testhost",
            "user": "testuser",
            "pass": "testpass",
            "path": "testpath"
        },
        1
    )


def test_worker_serve_in_view(worker) -> None:
    worker.door.isInView.return_value = True
    worker.door.isClosed.return_value = False
    worker.camera.hasUnstoredPicture.return_value = False
    worker._serve()
    worker.camera.takePicture.assert_called_once_with(
        round(worker.door.getAngle.return_value))
    worker.camera.storePictureAsFile.assert_not_called()
    worker.uploader.upload.assert_not_called()


def test_worker_serve_not_in_view(worker) -> None:
    worker.door.isInView.return_value = False
    worker.door.isClosed.return_value = False
    worker.camera.hasUnstoredPicture.return_value = False
    worker._serve()
    worker.camera.takePicture.assert_not_called()
    worker.camera.storePictureAsFile.assert_not_called()
    worker.uploader.upload.assert_not_called()


def test_worker_serve_closed(worker) -> None:
    worker.door.isInView.return_value = False
    worker.door.isClosed.return_value = True
    worker.camera.hasUnstoredPicture.return_value = False
    worker._serve()
    worker.camera.takePicture.assert_not_called()
    worker.camera.storePictureAsFile.assert_not_called()
    worker.uploader.upload.assert_not_called()


def test_worker_serve_closed_with_picture(worker) -> None:
    worker.door.isInView.return_value = False
    worker.door.isClosed.return_value = True
    worker.camera.hasUnstoredPicture.return_value = True
    worker._serve()
    worker.camera.takePicture.assert_not_called()
    worker.camera.storePictureAsFile.assert_called_once_with()
    worker.uploader.upload.assert_called_once_with(
        worker.camera.storePictureAsFile.return_value)
