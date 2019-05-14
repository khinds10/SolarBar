#! /usr/bin/python
# Solar Bar, color control sliders
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import sys, time, json, commands, subprocess, re, json, sys, os, memcache
from gpiozero import MCP3008
import includes.data as data
import RPi.GPIO as GPIO
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

# adjustable slider, so be it. you shall be the fellowship of the lamp
# https://projects.raspberrypi.org/en/projects/physical-computing/15
pot = MCP3008(0)
while True:
    
    # check to make sure that the alarm isn't ringing
    displayInUse = mc.get("INUSE")
    if displayInUse == "INUSE":
        print "alarm in use"
        time.sleep(1)
        continue
    
    # save current pot value to file for lamp to read
    print(pot.value)
    data.saveSliderPosition(str(int(pot.value * 100)))
    time.sleep(0.1)
