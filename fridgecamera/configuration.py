import argparse
import configparser
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional


def parse_arguments(
    args: Optional[List[str]],
    config_defaults: Dict[str, str],
) -> argparse.Namespace:
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action")
    run_parser = subparsers.add_parser("run", help="Run fridgecamera")
    subparsers.add_parser("calibrate", help="Calibrate door sensor")

    def _add_config_argument(name: str, **kwargs: Any) -> None:
        logger.debug(f"Adding config argument: {name}")
        if name in config_defaults:
            new_default = kwargs["type"](config_defaults[name])
            logger.debug(f"Setting new default: {new_default}")
            kwargs["default"] = new_default
        run_parser.add_argument(f"--{name}", **kwargs)

    parser.add_argument(
        "-v",
        "--verbose",
        help="Make logging more verbose",
        action="store_true",
        default=False,
    )
    parser.add_argument("--log_file", type=Path,
                        default=Path.home() / "fridgecamera.log",
                        help="Location for file log")

    # Camera
    _add_config_argument("camid", type=int, help="Camera ID", default=0)
    _add_config_argument("fps", type=int,
                         help="Images taken per second", default=2)

    # FTP
    _add_config_argument("ftp_host", type=str, default=None,
                         help="FTP host for uploading images")
    _add_config_argument("ftp_user", type=str,
                         default=None, help="User for FTP host")
    _add_config_argument("ftp_pass", type=str, default=None,
                         help="Password for FTP host")
    _add_config_argument("ftp_path", type=str, default=None,
                         help="Path on FTP host to save the images at")

    # Sensor
    _add_config_argument("sensor_min", type=int, default=12100,
                         help="Sensor value for open door")
    _add_config_argument("sensor_max", type=int, default=12800,
                         help="Sensor value for closed door")

    parsed = parser.parse_args(args)
    logger.debug(f"Got from command line ({args}): {parsed}")
    return parsed


def read_config_file(config_file: Path) -> Dict[str, str]:
    parser = configparser.ConfigParser()
    parser.read(config_file)
    parsed = dict(parser["DEFAULT"])
    logging.getLogger(__name__).debug(
        f"Got config from file ({config_file}): {parsed}")
    return parsed


def update_config_file(config: Dict[str, str], config_file: Path) -> None:
    logging.getLogger(__name__).debug(f"Updating {config_file} with: {config}")
    current = read_config_file(config_file)
    current.update(config)
    parser = configparser.ConfigParser(current)
    with open(config_file, "w") as f:
        parser.write(f)


def get_config(
    cli_str: Optional[List[str]],
    config_file: Optional[Path] = None,
) -> argparse.Namespace:
    config = read_config_file(config_file) if config_file else {}
    logging.getLogger(__name__).debug(f"Got {config} from file: {config_file}")
    return parse_arguments(cli_str, config)
