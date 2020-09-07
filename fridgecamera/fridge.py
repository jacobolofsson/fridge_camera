import cv2
import time
import datetime

OPTIMAL_DOOR_ANGLE = 45
DOOR_ANGLE_TOLERANCE = 5

class Door:
    def __init__(self):
        self.angle = 0
    def isClosed(self):
        return self.angle <= 0
    def isInView(self):
        # Compare squares instead of abs to skip sqrt operation
        return (self.angle-OPTIMAL_DOOR_ANGLE)**2 < DOOR_ANGLE_TOLERANCE**2
    def updateAngle(self):
        self.angle = readAngleSensor()
    def getAngle(self):
        return self.angle

class Image:
    def __init__(self, image, doorAngle):
        self.image = image
        self.timestamp = datetime.datetime.now()
        self.doorAngle = doorAngle
    def getFilename(self):
        return 'fridge_' + self.timestamp.strftime('%Y-%m-%d %H%M%S') + '.png' 

class Camera:
    def __init__(self, camID, imageFolderPath):
        self.camera = cv2.VideoCapture(camID)
        self.imgFolder = imageFolderPath
        self.imageList = []
        self.hasUnstoredImg = False
    def takePicture(self, angle):
        tmp, frame = self.camera.read()
        self.imageList.append(FridgeImage(frame, angle))
        self.hasUnstoredImg = True
    def storePictureAsFile(self):
        # The last image in the list is always the latest
        tempImg = self.imageList[-1]
        cv2.imwrite(self.imgFolder + tempImg.getFilename(), tempImg.image)
        del self.imageList[:]
        self.hasUnstoredImg = False
        return self.imgFolder, tempImg.getFilename()
    def hasUnstoredPicture(self):
        return self.hasUnstoredImg
