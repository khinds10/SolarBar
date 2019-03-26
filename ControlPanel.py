#! /usr/bin/python
# Solar Bar, control panel driver, handle button clicks, alarm being set
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, commands, subprocess, re, json, sys, os, memcache
import includes.data as data
from datetime import datetime
mc = memcache.Client(['127.0.0.1:11211'], debug=0)
from Adafruit_LED_Backpack import SevenSegment
import RPi.GPIO as GPIO

# setup alarm on / off LED
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16,GPIO.OUT)

# 7 Segment Clock on i2c on address 0x70
segment = SevenSegment.SevenSegment(address=0x71)

# initialize the display, must be called once before using the display
segment.begin()
segment.set_brightness(3)
segment.set_colon(True)

# get total number of gradients set for the light bar
path, dirs, files = next(os.walk("gradients"))
totalGradients = len(files)

def toggleAlarmOnLight(alarmSet):
    """toggle alarm on light"""
    print alarmSet
    if alarmSet == 'True':
        GPIO.output(16,GPIO.HIGH)
    else: 
        GPIO.output(16,GPIO.LOW)

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

# application values loaded from saved data on filesystem
alarm = data.getJSONFromDataFile('data/alarm.data')
sunriseTimeHour = alarm[0]
sunriseTimeMin = alarm[1]
alarmSet = data.getJSONFromDataFile('data/alarmSet.data')
gradientSet = data.getJSONFromDataFile('data/gradient.data')
lightOn = data.getJSONFromDataFile('data/lightOn.data')

# run script, check for button presses
toggleAlarmOnLight(alarmSet)
setDisplay(alarm[0], alarm[1])
countDown = 0
while True:

    # capture slider change from memcache flag update
    sliderValue = mc.get("SLIDER")
    if sliderValue is not "":
        print sliderValue        
        data.saveSliderPosition(sliderValue)

    # capture button press from memcache flag
    buttonPress = mc.get("BUTTON")
    if buttonPress is not "":
        print buttonPress

    # increase time by 15 min increments, increasing hour up to 23 hundred
    if buttonPress == "UP":
        countDown = 50
        sunriseTimeMin = sunriseTimeMin + 15
        if sunriseTimeMin > 45:
            sunriseTimeMin = 0
            sunriseTimeHour = sunriseTimeHour + 1
        if sunriseTimeHour > 23:
            sunriseTimeHour = 0

        # show new alarm time on 7 segment
        setDisplay(sunriseTimeHour, sunriseTimeMin)
        data.saveAlarmTime(sunriseTimeHour, sunriseTimeMin)

    # decrease time by 15 min increments, resetting hour back to 23 hundred
    if buttonPress == "DOWN":
        countDown = 50
        sunriseTimeMin = sunriseTimeMin - 15
        if sunriseTimeMin < 0:
            sunriseTimeMin = 45
            sunriseTimeHour = sunriseTimeHour - 1
        if sunriseTimeHour < 0:
            sunriseTimeHour = 23

        # show new alarm time on 7 segment
        setDisplay(sunriseTimeHour, sunriseTimeMin)
        data.saveAlarmTime(sunriseTimeHour, sunriseTimeMin)

    # turn on / off the alarm LED, save the settings to file
    elif buttonPress == "ALARM":
        if alarmSet == 'True':
            alarmSet = 'False'
            countDown = 0
        elif alarmSet == 'False':
            alarmSet = 'True'
            countDown = 50
        setDisplay(sunriseTimeHour, sunriseTimeMin)            
        toggleAlarmOnLight(alarmSet)
        data.saveAlarmSet(alarmSet)

    # turn on and off the light
    elif buttonPress == "LIGHT":
        lightOn = int(lightOn)
        lightOn = lightOn + 1
        if lightOn > 1:
            lightOn = 0
        data.saveLightOn(str(lightOn))

    # change the gradient set for the light panel
    elif buttonPress == "CHANGE":
        gradientSet = int(gradientSet)
        gradientSet = gradientSet + 1
        if gradientSet > totalGradients:
            gradientSet = 1
        data.saveGradientValue(str(gradientSet))

    # decrement the countDown value (we only keep the "time" 7 segment display on for so many seconds)
    countDown = countDown - 1
    if countDown < 0:
        countDown = 0
        segment.clear()
        segment.write_display()
        
    # wait and go around again
    mc.set("BUTTON", "")
    mc.set("SLIDER", "")
    
    time.sleep(0.1)
