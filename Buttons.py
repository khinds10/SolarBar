#! /usr/bin/python
# Solar Bar, buttons manager
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, commands, subprocess, re, json, sys, os, memcache
from gpiozero import Button
from datetime import datetime
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

# setup up button GPIO connections
upButton = Button(1)
downButton = Button(2)
alarmButton = Button(3)
lightButton = Button(4)

def pressUp():
    """up button pressed, increase sunrise time"""
    global mc
    mc.set("BUTTON", str("UP"))

def pressDown():
    """down button pressed, decrease sunrise time"""
    global mc
    mc.set("BUTTON", str("DOWN"))

def alarmOnOff():
    """alarm button pressed, turn on / off light alarm"""
    global mc
    mc.set("BUTTON", str("ALARM"))

def lightOnOff():
    """alarm button pressed, turn on / off light"""
    global mc
    mc.set("BUTTON", str("LIGHT"))

# run script, check for button presses
while True:
    upButton.when_pressed = pressUp
    downButton.when_pressed = pressDown
    alarmButton.when_pressed = alarmOnOff
    lightButton.when_pressed = lightOnOff
