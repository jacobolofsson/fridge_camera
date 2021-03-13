from unittest.mock import patch

from fridgecamera.configuration import read_config_file
from fridgecamera.main import main


@patch("fridgecamera.main.Worker")
def test_run(mock_worker, mock_tmp_dir, tmp_config_file, cli_args) -> None:
    assert main(cli_args) == 0

    mock_worker.assert_called_once_with(
        99,
        mock_tmp_dir / ".fridgecamera",
        (200, 12800),
        {
            "host": "testhost",
            "user": "testuser",
            "pass": None,
            "path": None,
        },
        123,
    )
    mock_worker.return_value.serve_forever.assert_called_once_with()


@patch("fridgecamera.main.Sensor")
def test_calibrate_existing_file(mock_sensor, tmp_config_file) -> None:
    new_min = 123
    new_max = 456
    mock_sensor.return_value.readValue.side_effect = (new_min, new_max)
    with patch("builtins.input"):
        main(["calibrate"])

    config = read_config_file(tmp_config_file)
    assert int(config["sensor_min"]) == new_min
    assert int(config["sensor_max"]) == new_max
