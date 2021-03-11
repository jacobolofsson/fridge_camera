import argparse
import logging
import pathlib
import tempfile
from typing import List, Optional

from fridgecamera.configuration import get_config, update_config_file
from fridgecamera.lock import FileLock
from fridgecamera.sensor import Sensor
from fridgecamera.worker import Worker


def ini_file_path() -> pathlib.Path:
    return pathlib.Path.home() / "fridgecamera.ini"


def run(args: argparse.Namespace) -> None:
    worker = Worker(
        args.camid,
        pathlib.Path(tempfile.gettempdir()) / ".fridgecamera",
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


def main(str_args: Optional[List[str]] = None) -> int:
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

    lock = FileLock()
    if not lock.acquire():
        logger.error("Instance of program is already running")
        return -3

    try:
        action(args)
    except KeyboardInterrupt:
        logger.info("Ctrl-C received")
    except Exception:
        logger.exception("An unhandled exception occurend!")
        return -1
    finally:
        lock.release()

    logger.info("Shutting down fridge camera")
    return 0
