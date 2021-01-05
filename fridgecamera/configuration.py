import argparse
import configparser
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional


def parse_arguments(
    args: List[str],
    config_defaults: Dict[str, str],
) -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    def _add_config_argument(name: str, **kwargs: Any) -> None:
        if name in config_defaults:
            kwargs["default"] = kwargs["type"](config_defaults[name])
        parser.add_argument(f"--{name}", **kwargs)

    parser.add_argument(
        "-v",
        "--verbose",
        help="Make logging more verbose",
        action="store_true",
        default=False,
    )
    _add_config_argument("camid", type=int, help="Camera ID", default=0)
    _add_config_argument("fps", type=int,
                         help="Images taken per second", default=2)

    _add_config_argument("ftp_host", type=str, default=None,
                         help="FTP host for uploading images")
    _add_config_argument("ftp_user", type=str,
                         default=None, help="User for FTP host")
    _add_config_argument("ftp_pass", type=str, default=None,
                         help="Password for FTP host")
    _add_config_argument("ftp_path", type=str, default=None,
                         help="Path on FTP host to save the images at")

    parsed = parser.parse_args(args)
    logging.getLogger(__name__).debug(
        f"Got from command line ({args}): {parsed}")
    return parsed


def read_config_file(config_file: Path) -> Dict[str, str]:
    parser = configparser.ConfigParser()
    parser.read(config_file)
    parsed = dict(parser["DEFAULT"])
    logging.getLogger(__name__).debug(f"Got config from file: {parsed}")
    return parsed


def update_config_file(config: Dict[str, str], config_file: Path) -> None:
    current = read_config_file(config_file)
    current.update(config)
    parser = configparser.ConfigParser(current)
    with open(config_file, "w") as f:
        parser.write(f)


def get_config(
    cli_str: List[str],
    config_file: Optional[Path] = None,
) -> argparse.Namespace:
    config = read_config_file(config_file) if config_file else {}
    return parse_arguments(cli_str, config)
