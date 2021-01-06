import argparse
import logging
import os
import pathlib
from tempfile import gettempdir
from typing import List

from fridgecamera.configuration import get_config, update_config_file
from fridgecamera.sensor import Sensor
from fridgecamera.worker import Worker


def ini_file_path() -> pathlib.Path:
    return pathlib.Path.home() / "fridgecamera.ini"


def run(args: argparse.Namespace) -> None:
    worker = Worker(
        args.camid,
        os.path.join(gettempdir(), ".fridgecamera"),
        (args.sensor_min, args.sensor_max),
        {
            "host": args.ftp_host,
            "user": args.ftp_user,
            "pass": args.ftp_pass,
            "path": args.ftp_path
        },
        args.fps
    )
    worker.serve_forever()


def calibrate(args: argparse.Namespace) -> None:
    sensor = Sensor(0, 0)

    def _prompt_value(prompt: str) -> int:
        input(f"{prompt}.\nPress enter to continue...")
        return sensor.readValue()

    min_val = _prompt_value("Fully open door")
    max_val = _prompt_value("Fully close door")

    update_config_file({"sensor_min": str(min_val),
                        "sensor_max": str(max_val)}, ini_file_path())


def main(str_args: List[str]) -> int:
    args = get_config(str_args, ini_file_path())

    logger = logging.getLogger("fridgecamera")
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(
        logging.DEBUG if args.verbose else logging.INFO
    )

    if args.action == "run":
        logger.info("Starting fridge camera")
        action = run
    elif args.action == "calibrate":
        logger.info("Starting sensor calibration")
        action = calibrate
    else:
        logger.error(f"Unknown action: {args.action}")
        return -2

    try:
        action(args)
    except KeyboardInterrupt:
        logger.info("Ctrl-C received")
    except Exception:
        logger.exception("An unhandled exception occurend!")
        return -1

    logger.info("Shutting down fridge camera")
    return 0
