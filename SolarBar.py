#! /usr/bin/python
# Solar Bar, main script
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, commands, subprocess, re, json, sys, os, memcache
from datetime import datetime
mc = memcache.Client(['127.0.0.1:11211'], debug=0)
from Adafruit_LED_Backpack import SevenSegment
import RPi.GPIO as GPIO

# setup alarm on / off LED
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

# 7 Segment Clock on i2c on address 0x70
segment = SevenSegment.SevenSegment(address=0x70)

# initialize the display, must be called once before using the display.
segment.begin()
segment.set_brightness(3)
segment.set_colon(True)

# application defaults
sunriseTimeHour = 7
sunriseTimeMin = 0
alarmOn = True
lightOn = False

def setDisplay(hour, minute):
    """set 7 segment display with hour and minute"""
    if (hour > 12):
        hour = hour - 12  
    segment.clear()
    segment.set_digit(0, int(hour / 10))
    segment.set_digit(1, hour % 10)
    segment.set_digit(2, int(minute / 10))
    segment.set_digit(3, minute % 10)
    segment.write_display()

# run script, check for button presses
while True:
    buttonPress = mc.get("BUTTON")

    # increase time by 15 min increments, increasing hour up to 23 hundred
    if buttonPress == "UP":
        sunriseTimeMin = sunriseTimeMin + 15
        if sunriseTimeMin > 45:
            sunriseTimeMin = 0
            sunriseTimeHour = sunriseTimeHour + 1
        if sunriseTimeHour > 23:
            sunriseTimeHour = 0

        # show new alarm time on 7 segment
        setDisplay(sunriseTimeHour, sunriseTimeMin)
        time.sleep(1)

    # decrease time by 15 min increments, resetting hour back to 23 hundred
    if buttonPress == "DOWN":
        sunriseTimeMin = sunriseTimeMin - 15
        if sunriseTimeMin < 0:
            sunriseTimeMin = 45
            sunriseTimeHour = sunriseTimeHour - 1
        if sunriseTimeHour < 0:
            sunriseTimeHour = 23

        # show new alarm time on 7 segment
        setDisplay(sunriseTimeHour, sunriseTimeMin)
        time.sleep(1)

    # turn on / off the alarm LED
    elif buttonPress == "ALARM":
        alarmOn = !alarmOn
        if alarmOn:
            GPIO.output(18,GPIO.HIGH)
        else: 
            GPIO.output(18,GPIO.LOW)

    # turn on and off the light
    elif buttonPress == "LIGHT":
        lightOn = !lightOn
    
    # set time on the clock
    now = datetime.datetime.now()
    setDisplay(now.hour, now.minute)
    
    # wait and go around again
    time.sleep(0.1)
