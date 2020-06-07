import RPi.GPIO as GPIO
import time
import datetime
import threading
import urllib.request
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.IN)
GPIO.setup(7, GPIO.OUT)
timer = 0
totalPeriodActiveDuration = 0

def thingspeak():
    val = totalPeriodActiveDuration
    URL = 'https://api.thingspeak.com/update?api_key='
    KEY = 'KO9JUF5D5IFNNNJ6'
    HEADER='&field1={}'.format(val)
    NEW_URL = URL+KEY+HEADER
    data=urllib.request.urlopen(NEW_URL)
    print(NEW_URL)

def perpetualUpdate():
    thingspeak()
    global totalPeriodActiveDuration
    totalPeriodActiveDuration = 0
    threading.Timer(60, perpetualUpdate).start()

threading.Timer(60, perpetualUpdate).start()
try:
    while True:
        print('Timer: ' + str(timer))
        print('Active Duration: ' + str(totalPeriodActiveDuration))
        if GPIO.input(18):
            timer = 10
        else:
            timer -= 0.5
        if timer > 0:
            GPIO.output(7, GPIO.HIGH)
            totalPeriodActiveDuration += 0.5
        else:
            GPIO.output(7, GPIO.LOW)
        time.sleep(0.5)
except KeyboardInterrupt:
    print('Finished!')
GPIO.cleanup()
