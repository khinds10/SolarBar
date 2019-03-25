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
upButton = Button(21)
downButton = Button(20)
alarmButton = Button(19)
lightButton = Button(26)
changeButton = Button(13)

def pressUp():
    """up button pressed, increase sunrise time"""
    mc.set("BUTTON", str("UP"))

def pressDown():
    """down button pressed, decrease sunrise time"""
    mc.set("BUTTON", str("DOWN"))

def alarmOnOff():
    """alarm button pressed, turn on / off light alarm"""
    mc.set("BUTTON", str("ALARM"))

def lightOnOff():
    """alarm button pressed, turn on / off light"""
    mc.set("BUTTON", str("LIGHT"))

def changeGradient():
    """change gradient button pressed, change gradient"""
    mc.set("BUTTON", str("CHANGE"))

while True:
    upButton.when_pressed = pressUp
    downButton.when_pressed = pressDown
    alarmButton.when_pressed = alarmOnOff
    lightButton.when_pressed = lightOnOff
    changeButton.when_pressed = changeGradient
    time.sleep(0.1)
