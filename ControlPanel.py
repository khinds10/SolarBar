#! /usr/bin/python
# Solar Bar, control panel driver, handle button clicks, alarm being set
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, commands, subprocess, re, json, sys, os, memcache, datetime
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
path, dirs, files = next(os.walk("/home/pi/SolarBar/gradients"))
totalGradients = len(files)

def toggleAlarmOnLight(alarmSet):
    """toggle alarm on light"""
    print alarmSet
    if alarmSet == 'True':
        GPIO.output(16,GPIO.HIGH)
    else: 
        GPIO.output(16,GPIO.LOW)

def setDisplay(hour, minute, brightness):
    """set 7 segment display with hour and minute"""
    if (hour > 12):
        hour = hour - 12  
    segment.clear()
    segment.set_digit(0, int(hour / 10))
    segment.set_digit(1, hour % 10)
    segment.set_digit(2, int(minute / 10))
    segment.set_digit(3, minute % 10)
    segment.set_colon(True)
    segment.set_brightness(brightness)
    segment.write_display()
    
def setDisplayMessage(digit1, digit2, digit3, digit4, brightness):
    """set the display to show custom message digit by digit"""
    segment.clear()
    segment.set_digit(0, digit1)
    segment.set_digit(1, digit2)
    segment.set_digit(2, digit3)
    segment.set_digit(3, digit4)
    segment.set_colon(False)
    segment.set_brightness(brightness)
    segment.write_display()

# application values loaded from saved data on filesystem
alarm = data.getJSONFromDataFile('/home/pi/SolarBar/data/alarm.data')
sunriseTimeHour = alarm[0]
sunriseTimeMin = alarm[1]
alarmSet = data.getJSONFromDataFile('/home/pi/SolarBar/data/alarmSet.data')
gradientSet = data.getJSONFromDataFile('/home/pi/SolarBar/data/gradient.data')
lightOn = data.getJSONFromDataFile('/home/pi/SolarBar/data/lightOn.data')

# run script, check for button presses
toggleAlarmOnLight(alarmSet)
countDown = 0
while True:

    # capture slider change from memcache flag update
    sliderValue = mc.get("SLIDER")
    if sliderValue is not "":
        print sliderValue
        
        #TODO get the slider reversed and have it show 0-100 here
        
        #TODO is this even used!?
        # i think you have to get it from the file directly
        
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
        setDisplay(sunriseTimeHour, sunriseTimeMin, 3)
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
        countDown = 50
        lightOn = int(lightOn)
        lightOn = lightOn + 1
        if lightOn > 1:
            lightOn = 0
        data.saveLightOn(str(lightOn))
        
        # show the on/off state on the LED display
        if lightOn > 0:
            setDisplayMessage("", "", "o", "n", 3)
        else:
            setDisplayMessage("", "o", "f", "f", 3)
        
    # change the gradient set for the light panel
    elif buttonPress == "CHANGE":
        countDown = 50
        gradientSet = int(gradientSet)
        gradientSet = gradientSet + 1
        if gradientSet > totalGradients:
            gradientSet = 1
        data.saveGradientValue(str(gradientSet))
        
        # show the current gradient number on the LED display
        setDisplayMessage("-", "-", "-", str(gradientSet), 3)
        
    # decrement the countDown value (we only keep the "time" 7 segment display on for so many seconds)
    countDown = countDown - 1
    if countDown < 0:
        countDown = 0
        now = datetime.datetime.now()
        setDisplay(str(now.hour), str(now.minute), 1)
        
    # wait and go around again
    mc.set("BUTTON", "")
    mc.set("SLIDER", "")
    
    time.sleep(0.1)
