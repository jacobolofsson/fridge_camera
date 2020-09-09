import datetime
import logging
from typing import Tuple

import cv2
import numpy

from fridgecamera.sensor import Sensor

OPTIMAL_DOOR_ANGLE = 5
DOOR_ANGLE_TOLERANCE = 5
DOOR_CLOSED_ANGLE = 60


class Door:
    def __init__(self) -> None:
        self.angle = 0.0
        self.sensor = Sensor()
        self.logger = logging.getLogger(__name__)

    def isClosed(self) -> bool:
        self.logger.debug(f"Angle: {self.angle} >= {DOOR_CLOSED_ANGLE}")
        return self.angle >= DOOR_CLOSED_ANGLE

    def isInView(self) -> bool:
        # Compare squares instead of abs to skip sqrt operation
        return (self.angle - OPTIMAL_DOOR_ANGLE)**2 < DOOR_ANGLE_TOLERANCE**2

    def updateAngle(self) -> None:
        self.angle = self.sensor.readAngle()

    def getAngle(self) -> float:
        return self.angle


class Image:
    def __init__(self, image: numpy.ndarray, doorAngle: int) -> None:
        self.image = image
        self.timestamp = datetime.datetime.now()
        self.doorAngle = doorAngle

    def getFilename(self) -> str:
        return 'fridge_' + self.timestamp.strftime('%Y-%m-%d %H%M%S') + '.png'


class Camera:
    def __init__(self, camID: int, imageFolderPath: str) -> None:
        self.camera = cv2.VideoCapture(camID)
        self.imgFolder = imageFolderPath
        self.hasUnstoredImg = False

    def takePicture(self, angle: int) -> None:
        _, frame = self.camera.read()
        self.currentImage = Image(frame, angle)
        self.hasUnstoredImg = True

    def storePictureAsFile(self) -> Tuple[str, str]:
        # The last image in the list is always the latest
        cv2.imwrite(
            self.imgFolder +
            self.currentImage.getFilename(),
            self.currentImage.image)
        self.hasUnstoredImg = False
        return self.imgFolder, self.currentImage.getFilename()

    def hasUnstoredPicture(self) -> bool:
        return self.hasUnstoredImg
