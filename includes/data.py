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
    f = file('data/alarm.data', "w")
    alarmTime = [hour, minute]
    f.write(str(json.dumps(alarmTime)))

def saveAlarmOn(alarmOn):
    """save if the alarm is turned on or off"""
    f = file('data/alarmSet.data', "w")
    f.write(str(json.dumps(alarmOn)))
    
def saveLightOn(lightOn):
    """save if the light is turned on or off"""
    f = file('data/lightOn.data', "w")
    f.write(str(json.dumps(lightOn)))
