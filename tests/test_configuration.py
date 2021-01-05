from fridgecamera.configuration import get_config, update_config_file

default_config = {
    "verbose": False,
    "camid": 0,
    "fps": 2,
    "sensor_max": 12800,
    "sensor_min": 12100,
    "ftp_host": None,
    "ftp_user": None,
    "ftp_pass": None,
    "ftp_path": None,
}

cli_config = {
    "verbose": True,
    "camid": 99,
    "fps": 123,
    "ftp_host": "testhost",
}


def test_default_args() -> None:
    args = get_config([])
    assert vars(args) == default_config


def test_parse_args(cli_args) -> None:
    args = get_config(cli_args)
    expected = default_config.copy()
    expected.update(cli_config)
    assert vars(args) == expected


def test_no_config_file(tmp_path) -> None:
    non_existing_file_path = tmp_path / "fridgecamera.ini"
    args = get_config([], non_existing_file_path)
    assert vars(args) == default_config


def test_parse_config_file(tmp_config_file, file_config) -> None:
    args = get_config([], tmp_config_file)
    expected = default_config.copy()
    expected.update(file_config)
    assert vars(args) == expected


def test_parse_args_with_file(tmp_config_file, file_config, cli_args) -> None:
    args = get_config(cli_args, tmp_config_file)
    expected = default_config.copy()
    expected.update(file_config)
    expected.update(cli_config)
    assert vars(args) == expected


def test_update_config_file(tmp_config_file) -> None:
    key = "fps"
    value = 5000
    update_config_file({key: value}, tmp_config_file)
    args = get_config([], tmp_config_file)
    assert vars(args)[key] == value
