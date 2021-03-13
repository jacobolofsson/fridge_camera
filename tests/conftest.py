from typing import Dict, List
from unittest.mock import MagicMock, patch

import pytest

# Patch HW-specific modules
patch.dict(
    "sys.modules",
    {
        "board": MagicMock(),
        "busio": MagicMock(),
        "adafruit_ads1x15": MagicMock(),
        "adafruit_ads1x15.ads1115": MagicMock(),
        "adafruit_ads1x15.analog_in": MagicMock(),
    }
).start()


@pytest.fixture()
def cli_args() -> List[str]:
    return [
        "-v",
        "run",
        "--camid",
        "99",
        "--fps",
        "123",
        "--ftp_host",
        "testhost",
    ]


@pytest.fixture()
def file_config() -> Dict[str, object]:
    return {
        "camid": 666,
        "ftp_user": "testuser",
        "sensor_min": 200,
    }


@pytest.fixture()
def tmp_config_file(mock_home_dir, file_config):
    content = "[DEFAULT]\n"
    for k, v in file_config.items():
        content += f"{k} = {v}\n"

    config_file = mock_home_dir / "fridgecamera.ini"
    config_file.write_text(content)
    return config_file


@pytest.fixture(autouse=True)
def mock_home_dir(tmp_path):
    path = tmp_path / "mock_home"
    path.mkdir()
    with patch("pathlib.Path.home") as mock_home:
        mock_home.return_value = path
        yield path


@pytest.fixture(autouse=True)
def mock_tmp_dir(tmp_path):
    path = tmp_path / "mock_temp"
    path.mkdir()
    with patch("tempfile.gettempdir") as mock_tmpdir:
        mock_tmpdir.return_value = str(path)
        yield path
