import logging
import os
from tempfile import gettempdir
from typing import List

from fridgecamera.configuration import parse_arguments
from fridgecamera.worker import Worker


def main(str_args: List[str]) -> int:
    args = parse_arguments(str_args)

    logger = logging.getLogger("fridgecamera")
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(
        logging.DEBUG if args.verbose else logging.INFO
    )

    worker = Worker(
        args.camid,
        os.path.join(gettempdir(), ".fridgecamera"),
        {
            "host": args.ftp_host,
            "user": args.ftp_user,
            "pass": args.ftp_pass,
            "path": args.ftp_path
        },
        args.fps
    )

    logger.info("Starting fridge camera")
    try:
        worker.serve_forever()
    except KeyboardInterrupt:
        logger.info("Ctrl-C received")
    except Exception:
        logger.exception("An unexpected exception occurend!")
        return -1

    logger.info("Shutting down fridge camera")
    return 0
