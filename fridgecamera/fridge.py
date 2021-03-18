import datetime
import logging
import pathlib
from typing import TYPE_CHECKING

import cv2
import numpy

if TYPE_CHECKING:
    from fridgecamera.sensor import Sensor

OPTIMAL_DOOR_ANGLE = 5
DOOR_ANGLE_TOLERANCE = 5
DOOR_CLOSED_ANGLE = 60


class Door:
    def __init__(self, sensor: "Sensor") -> None:
        self.angle = 0.0
        self.sensor = sensor
        self.logger = logging.getLogger(__name__)

    def isClosed(self) -> bool:
        self.logger.debug(f"Angle: {self.angle} >= {DOOR_CLOSED_ANGLE}")
        return self.angle >= DOOR_CLOSED_ANGLE

    def isInView(self) -> bool:
        diff = abs(self.angle - OPTIMAL_DOOR_ANGLE)
        self.logger.debug(f"Diff: {diff} Tolerance: {DOOR_ANGLE_TOLERANCE}")
        return diff < DOOR_ANGLE_TOLERANCE

    def updateAngle(self) -> None:
        self.angle = self.sensor.readAngle()

    def getAngle(self) -> float:
        return self.angle


class Image:
    def __init__(self, image: numpy.ndarray, doorAngle: int) -> None:
        self.image = image
        self.timestamp = datetime.datetime.now()
        self.doorAngle = doorAngle
        logging.getLogger(__name__).info(
            f"Creating image at angle: {doorAngle} with "
            f"timestamp: {self.timestamp}",
        )

    def getFilename(self) -> str:
        return 'fridge_' + self.timestamp.strftime('%Y-%m-%d %H%M%S') + '.png'


class Camera:
    def __init__(self, camID: int, imageFolderPath: pathlib.Path) -> None:
        self.camera = cv2.VideoCapture(camID)
        self.imgFolder = imageFolderPath
        self.hasUnstoredImg = False
        self.logger = logging.getLogger(__name__)

    def takePicture(self, angle: int) -> None:
        self.logger.info("Taking picture")
        _, frame = self.camera.read()
        self.currentImage = Image(frame, angle)
        self.hasUnstoredImg = True

    def storePictureAsFile(self) -> pathlib.Path:
        # The last image in the list is always the latest
        imgname = self.currentImage.getFilename()
        self.logger.info(f"Storing picture {imgname} at: {self.imgFolder}")

        # Make sure cv2 dont fail because directory doesn't exist
        self.imgFolder.mkdir(parents=True, exist_ok=True)

        imgPath = self.imgFolder / imgname
        if not cv2.imwrite(str(imgPath), self.currentImage.image):
            raise RuntimeError(f"Failed to write picture to disk: {imgPath}")

        self.hasUnstoredImg = False
        return imgPath

    def hasUnstoredPicture(self) -> bool:
        return self.hasUnstoredImg
