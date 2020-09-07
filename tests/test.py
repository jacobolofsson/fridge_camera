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
        return (self.angle-OPTIMAL_DOOR_ANGLE)**2 < DOOR_ANGLE_TOLERANCE**2
    def update(self, angle):
        self.angle = angle
    def getAngle(self):
        return self.angle

class FridgeImage:
    def __init__(self, image, doorAngle):
        self.image = image
        self.timestamp = datetime.datetime.now()
        self.doorAngle = doorAngle
    def getFilename(self):
        return 'fridge_' + self.timestamp.strftime('%Y%m%d_%H%M%S') + '.png' 

fridgeDoor = FridgeDoor()
fridgeImgList = []
camera = cv2.VideoCapture(0)
hasUnsentImage = False

while(1):
    fridgeDoor.update(readAngleSensor())
    if(fridgeDoor.isInView()):
        ret, frame = camera.read()
        newImage = FridgeImage(frame, fridgeDoor.getAngle())
        # No need to use list?
        fridgeImgList.append(newImage)
        hasUnsentImage = True
    elif(fridgeDoor.isClosed() and hasUnsentImage): #Wait until door is closed to send image
        img = fridgeImgList[-1]

        cv2.imwrite(img.getFilename(), img.image)

        ftps = ftplib.FTP(host='ftp.gransta.se')
        ftps.login(user='gransta.se', passwd='#PgqyOGM')
        ftps.cwd('/fridge')

        image_fd = open(img.getFilename(), 'rb');
        ftps.storbinary('STOR ' + img.getFilename(), image_fd);

        image_fd.close()
        ftps.quit()
        del fridgeImgList[:]
        hasUnsentImage = False

    time.sleep(0.5)

camera.release()
