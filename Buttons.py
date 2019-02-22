#! /usr/bin/python
# Solar Bar, buttons manager
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, commands, subprocess, re, json, sys, os, memcache, json
import includes.data as data
from gpiozero import Button
from gpiozero import LED
from datetime import datetime
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

# setup up button GPIO connections
upButton = Button(20)
downButton = Button(21)
alarmButton = Button(19)
lightButton = Button(26)

def pressUp():
    """up button pressed, increase sunrise time"""
    global mc
    print "UP"
    mc.set("BUTTON", str("UP"))

def pressDown():
    """down button pressed, decrease sunrise time"""
    global mc
    print "DOWN"
    mc.set("BUTTON", str("DOWN"))

def alarmOnOff():
    """alarm button pressed, turn on / off light alarm"""
    global mc
    print "ALARM"
    mc.set("BUTTON", str("ALARM"))

def lightOnOff():
    """alarm button pressed, turn on / off light"""
    global mc
    print "LIGHT"
    mc.set("BUTTON", str("LIGHT"))

while True:
    upButton.when_pressed = pressUp
    downButton.when_pressed = pressDown
    alarmButton.when_pressed = alarmOnOff
    lightButton.when_pressed = lightOnOff
    time.sleep(0.1)
