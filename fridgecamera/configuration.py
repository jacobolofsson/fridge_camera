import argparse
from typing import List


def parse_arguments(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        help="Make logging more verbose",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-p",
        "--imgpath",
        help="Path for images",
        default="images/",
    )
    parser.add_argument("--camid", type=int, help="Camera ID", default=0)
    parser.add_argument("--fps", type=int,
                        help="Images taken per second", default=2)

    parser.add_argument("--ftp_host", type=str, default=None,
                        help="FTP host for uploading images")
    parser.add_argument("--ftp_user", type=str,
                        default=None, help="User for FTP host")
    parser.add_argument("--ftp_pass", type=str, default=None,
                        help="Password for FTP host")
    parser.add_argument("--ftp_path", type=str, default=None,
                        help="Path on FTP host to save the images at")

    return parser.parse_args(args)
