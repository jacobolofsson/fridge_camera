import ftplib
import cv2
import time
import datetime

OPTIMAL_DOOR_ANGLE = 45
DOOR_ANGLE_TOLERANCE = 5

def readAngleSensor():
    return int(input('Enter door angle:'))

class FridgeDoor:
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

class FridgeImage:
    def __init__(self, image, doorAngle):
        self.image = image
        self.timestamp = datetime.datetime.now()
        self.doorAngle = doorAngle
    def getFilename(self):
        return 'fridge_' + self.timestamp.strftime('%Y%m%d_%H%M%S') + '.png' 

class FridgeCamera:
    def __init__(self, camID):
        self.camera = cv2.VideoCapture(camID)
        self.imageList = []
        self.hasUnstoredImg = False
    def takePicture(self, angle):
        tmp, frame = self.camera.read()
        self.imageList.append(FridgeImage(frame, angle))
        self.hasUnstoredImg = True
    def storePictureAsFile(self):
        # The last image in the list is always the latest
        tempImg = self.imageList[-1]
        cv2.imwrite(tempImg.getFilename(), tempImg.image)
        del self.imageList[:]
        self.hasUnstoredImg = False
        return tempImg.getFilename()
    def hasUnstoredPicture(self):
        return self.hasUnstoredImg

class ImageUploader:
    def __init__(self, host, user, passwd, path):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.path = path
    def upload(self, filename):
        # Open and close FTP connection for each transfer.
        # Might be a long time between transmissions.
        ftps = ftplib.FTP(host=self.host)
        ftps.login(user=self.user, passwd=self.passwd)
        ftps.cwd(self.path)
        image_fd = open(filename, 'rb');
        # Use same file name at destination as source
        ftps.storbinary('STOR ' + filename, image_fd);
        image_fd.close()
        ftps.quit()

### START OF SCRPIT ###
fridgeDoor = FridgeDoor()
fridgeCamera = FridgeCamera(0)
uploader = ImageUploader(
        'ftp.gransta.se',
        'gransta.se',
        '#PgqyOGM',
        '/fridge')


while(1):
    fridgeDoor.updateAngle()
    if(fridgeDoor.isInView()):
        fridgeCamera.takePicture(fridgeDoor.getAngle())
    # Wait until door is closed to send image, to prevent unnecesary uploads
    elif(fridgeDoor.isClosed() and fridgeCamera.hasUnstoredPicture()): 
        filename = fridgeCamera.storePictureAsFile()
        uploader.upload(filename)

    time.sleep(0.5)

camera.release()
