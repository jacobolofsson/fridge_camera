import sys
import argparse

import fridgecamera.fridge as fridge
import fridgecamera.uploader as uploader

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", , "--imgpath", help="Path for images", default="images/")
    parser.add_argument("--camid", help="Camera ID", default=0)
    parser.add_argument("--fps", help="Images taken per second", default=2)

    return parser.parse_args()

def main() -> int:
    args = parse_arguments()

    fridgeDoor = fridge.Door()
    fridgeCamera = fridge.Camera(args.camid, args.imgpath)
    uploader = uploader.Uploader(
        config.FTP_HOST,
        config.FTP_USER,
        config.FTP_PASS,
        config.FTP_PATH,
    )

    while(1):
        fridgeDoor.updateAngle()
        if(fridgeDoor.isInView()):
            fridgeCamera.takePicture(fridgeDoor.getAngle())
        # Wait until door is closed to send image, to prevent unnecesary uploads
        elif(fridgeDoor.isClosed() and fridgeCamera.hasUnstoredPicture()): 
            path, filename = fridgeCamera.storePictureAsFile()
            uploader.upload(path, filename)

        time.sleep(1/args.fps)

    camera.release()
    return 0

if __name__ == "__main__":
    sys.exit(main())
