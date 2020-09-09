import argparse
import sys
import time

import fridgecamera.fridge as fridge
import fridgecamera.uploader as uploader


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--imgpath",
        help="Path for images",
        default="images/",
    )
    parser.add_argument("--camid", help="Camera ID", default=0)
    parser.add_argument("--fps", help="Images taken per second", default=2)

    return parser.parse_args()


def main() -> int:
    args = parse_arguments()

    fridgeDoor = fridge.Door()
    fridgeCamera = fridge.Camera(args.camid, args.imgpath)
    imgUploader = uploader.Uploader(
        args.FTP_HOST,
        args.FTP_USER,
        args.FTP_PASS,
        args.FTP_PATH,
    )

    while(1):
        fridgeDoor.updateAngle()
        if(fridgeDoor.isInView()):
            fridgeCamera.takePicture(round(fridgeDoor.getAngle()))
        # Wait until door is closed to send image, to prevent unnecesary
        # uploads
        elif(fridgeDoor.isClosed() and fridgeCamera.hasUnstoredPicture()):
            path, filename = fridgeCamera.storePictureAsFile()
            imgUploader.upload(path, filename)

        time.sleep(1 / args.fps)
    return 0


if __name__ == "__main__":
    sys.exit(main())
