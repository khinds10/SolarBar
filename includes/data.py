#! /usr/bin/python
# Data helper functions to save and load application settings on the file system
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, json, string, cgi, subprocess, os

def getJSONFromDataFile(fileName):
    """get JSON contents from file in question"""
    try:
        with open(fileName) as locationFile:    
            return json.load(locationFile)
    except (Exception):
        return ""

def saveAlarmTime(hour, minute):
    """save the hour and minutes the sunrise alarm is set to"""
    f = file('/home/pi/SolarBar/data/alarm.data', "w")
    alarmTime = [hour, minute]
    f.write(str(json.dumps(alarmTime)))

def saveAlarmSet(alarmSet):
    """save if the alarm is turned on or off"""
    f = file('/home/pi/SolarBar/data/alarmSet.data', "w")
    f.write(str(json.dumps(alarmSet)))

def saveLightOn(lightOn):
    """save if the light is turned on or off"""
    f = file('/home/pi/SolarBar/data/lightOn.data', "w")
    f.write(str(json.dumps(lightOn)))

def saveGradientValue(gradientSet):
    """save which gradient to show on the panel"""
    f = file('/home/pi/SolarBar/data/gradient.data', "w")
    f.write(str(json.dumps(gradientSet)))
    
def saveSliderPosition(sliderValue):
    """save current position the slider is set to"""
    f = file('/home/pi/SolarBar/data/position.data', "w")
    f.write(str(json.dumps(sliderValue)))
