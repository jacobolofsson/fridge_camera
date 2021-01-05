import time
from typing import Dict, Tuple

from fridgecamera.fridge import Camera, Door
from fridgecamera.sensor import Sensor
from fridgecamera.uploader import Uploader


class Worker:
    def __init__(
        self,
        camid: int,
        imgpath: str,
        sensor_config: Tuple[int, int],
        ftp_details: Dict[str, str],
        fps: int
    ) -> None:
        self.door = Door(Sensor(*sensor_config))
        self.camera = Camera(camid, imgpath)
        self.uploader = Uploader(
            ftp_details["host"],
            ftp_details["user"],
            ftp_details["pass"],
            ftp_details["path"],
        )
        self.fps = fps
        self.stop = False

    def serve_forever(self) -> None:
        while (not self.stop):
            self._serve()

    def _serve(self) -> None:
        self.door.updateAngle()
        if(self.door.isInView()):
            self.camera.takePicture(round(self.door.getAngle()))
        # Wait until door is closed to send image, to prevent unnecesary
        # uploads
        elif(self.door.isClosed() and self.camera.hasUnstoredPicture()):
            path, filename = self.camera.storePictureAsFile()
            self.uploader.upload(path, filename)

        time.sleep(1 / self.fps)
