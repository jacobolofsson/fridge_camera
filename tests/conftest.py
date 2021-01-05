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
def tmp_config_file(tmp_path, file_config):
    content = "[DEFAULT]\n"
    for k, v in file_config.items():
        content += f"{k} = {v}\n"

    config_file = tmp_path / "fridgecamera.ini"
    config_file.write_text(content)

    return config_file
