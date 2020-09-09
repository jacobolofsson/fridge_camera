import time

import adafruit_ads1x15.ads1115 as ADS
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)


ads = ADS.ADS1115(i2c)

MAX = 20000
MIN = 10000
while(1):
    chan = AnalogIn(ads, ADS.P0)
    angle = (chan.value - MIN) * 90 / (MAX - MIN)
    print(angle, chan.value)
    time.sleep(0.5)
