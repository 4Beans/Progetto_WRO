import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

def reset():
    GPIO.output(comunicaReset,GPIO.HIGH)
    print("reset")
    time.sleep(0.1)
    GPIO.output(comunicaReset,GPIO.LOW)
    
def destra90():
    GPIO.output(comDx90,GPIO.HIGH)
    print("destra90")
    time.sleep(0.1)
    GPIO.output(comDx90,GPIO.LOW)
    
def sinistra90():
    GPIO.output(comSx90,GPIO.HIGH)
    print("sinistra90")
    time.sleep(0.1)
    GPIO.output(comSx90,GPIO.LOW)

def destra():
    GPIO.output(comDx,GPIO.HIGH)
    print("destra")
    time.sleep(0.1)
    GPIO.output(comDx,GPIO.LOW)
    
def sinistra():
    GPIO.output(comSx,GPIO.HIGH)
    print("sinistra")
    time.sleep(0.1)
    GPIO.output(comSx,GPIO.LOW)
    
def stop():
    GPIO.output(comunicaStop,GPIO.HIGH)
    print("stop")
    time.sleep(1)
    GPIO.output(comunicaStop,GPIO.LOW)

tastoReset=2
comunicaReset=3
comDx90=4
comSx90=17
comDx=27
comSx=22
comunicaStop=26

GPIO.setup(comunicaReset,GPIO.OUT)
GPIO.setup(comDx90,GPIO.OUT)
GPIO.setup(comSx90,GPIO.OUT)
GPIO.setup(comDx,GPIO.OUT)
GPIO.setup(comSx,GPIO.OUT)
GPIO.setup(comunicaStop,GPIO.OUT)
GPIO.setup(tastoReset, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(comunicaReset,GPIO.LOW)
GPIO.output(comDx90,GPIO.LOW)
GPIO.output(comSx90,GPIO.LOW)
GPIO.output(comDx,GPIO.LOW)
GPIO.output(comSx,GPIO.LOW)
GPIO.output(comunicaStop,GPIO.LOW)
