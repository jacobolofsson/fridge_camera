import ftplib
import cv2
import time
import datetime

import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

MAX_ANGLE = 90
MAX_SENSOR_VAL = 20000
MIN_SENSOR_VAL = 10000
def valueToAngle(value):
    return (value-MIN_SENSOR_VAL)*MAX_ANGLE/(MAX_SENSOR_VAL - MIN_SENSOR_VAL)

class DoorSensor():
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = ADS.ADS1115(i2c)
    def readAngle(self):
        chan = AnalogIn(self.sensor, ADS.P0)
        angle = valueToAngle(chan.value)
        print("Angle: ", angle, "Value:", chan.value)
        return angle


# import FTP config from external file
import config

OPTIMAL_DOOR_ANGLE = 45
DOOR_ANGLE_TOLERANCE = 5
DOOR_CLOSED_ANGLE = 10

class FridgeDoor:
    def __init__(self):
        self.angle = 0
    def isClosed(self):
        return self.angle <= DOOR_CLOSED_ANGLE
    def isInView(self):
        # Compare squares instead of abs to skip sqrt operation
        return (self.angle-OPTIMAL_DOOR_ANGLE)**2 < DOOR_ANGLE_TOLERANCE**2
    def updateAngle(self, angle):
        self.angle = angle
    def getAngle(self):
        return self.angle

class FridgeImage:
    def __init__(self, image, doorAngle):
        self.image = image
        self.timestamp = datetime.datetime.now()
        self.doorAngle = doorAngle
    def getFilename(self):
        return 'fridge_' + self.timestamp.strftime('%Y-%m-%d %H%M%S') + '.png' 

class FridgeCamera:
    def __init__(self, camID, imageFolderPath):
        self.camera = cv2.VideoCapture(camID)
        self.imgFolder = imageFolderPath
        self.hasUnstoredImg = False
        
    def takePicture(self, angle):
        tmp, frame = self.camera.read()
        self.currentImage = FridgeImage(frame, angle)
        self.hasUnstoredImg = True

    def storePictureAsFile(self):
        # The last image in the list is always the latest
        cv2.imwrite(self.imgFolder + self.currentImage.getFilename(), self.currentImage.image)
        self.hasUnstoredImg = False
        return self.imgFolder, self.currentImage.getFilename()

    def hasUnstoredPicture(self):
        return self.hasUnstoredImg

class ImageUploader:
    def __init__(self, host, user, passwd, path):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.path = path
    def upload(self, filepath, filename):
        # Open and close FTP connection for each transfer.
        # Might be a long time between transmissions.
        ftps = ftplib.FTP(host=self.host)
        ftps.login(user=self.user, passwd=self.passwd)
        ftps.cwd(self.path)
        image_fd = open(filepath + filename, 'rb');
        # Use same file name at destination as source
        ftps.storbinary('STOR ' + filename, image_fd);
        image_fd.close()
        ftps.quit()

### START OF SCRPIT ###
fridgeDoor = FridgeDoor()
doorSensor = DoorSensor()
fridgeCamera = FridgeCamera(0, 'images/')
uploader = ImageUploader(
    config.FTP_HOST,
    config.FTP_USER,
    config.FTP_PASS,
    config.FTP_PATH)

while(1):
    fridgeDoor.updateAngle(doorSensor.readAngle())
    if(fridgeDoor.isInView()):
        fridgeCamera.takePicture(fridgeDoor.getAngle())
        print("Taking picture")
    # Wait until door is closed to send image, to prevent unnecesary uploads
    elif(fridgeDoor.isClosed() and fridgeCamera.hasUnstoredPicture()): 
        path, filename = fridgeCamera.storePictureAsFile()
        uploader.upload(path, filename)
        print("Uploading picture")

    time.sleep(0.5)

camera.release()
