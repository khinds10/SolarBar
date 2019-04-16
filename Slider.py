#! /usr/bin/python
# Solar Bar, color control sliders
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, json #, commands, subprocess, re, json, sys, os, memcache
#import includes.data as data
import RPi.GPIO as GPIO
#mc = memcache.Client(['127.0.0.1:11211'], debug=0)

# adjustable slider, so be it. you shall be the fellowship of the lamp
# http://razzpisampler.oreilly.com/ch08.html
GPIO.setmode(GPIO.BCM)
a_pin = 18
b_pin = 23

def discharge():
    GPIO.setup(a_pin, GPIO.IN)
    GPIO.setup(b_pin, GPIO.OUT)
    GPIO.output(b_pin, False)
    time.sleep(0.005)

def chargeTime():
    GPIO.setup(b_pin, GPIO.IN)
    GPIO.setup(a_pin, GPIO.OUT)
    count = 0
    GPIO.output(a_pin, True)
    while not GPIO.input(b_pin):
        count = count + 1
    return count

def analogRead():
    discharge()
    return chargeTime()

def getCurrentGradient(currentGradient):
    if currentGradient < 1:
        currentGradient = 1
    if currentGradient > 25:
        currentGradient = 25
    ledNewGradient = currentGradient * 12
    currentGradient = int(getJSONFromDataFile('/home/pi/SolarBar/data/position.data'))
    if (ledNewGradient > currentGradient + 12 or ledNewGradient < currentGradient - 12):
        saveSliderPosition(str(ledNewGradient))
        print ledNewGradient

def saveSliderPosition(sliderValue):
    """save current position the slider is set to"""
    f = file('/home/pi/SolarBar/data/position.data', "w")
    f.write(str(json.dumps(sliderValue)))

def getJSONFromDataFile(fileName):
    """get JSON contents from file in question"""
    try:
        with open(fileName) as locationFile:    
            return json.load(locationFile)
    except (Exception):
        return ""

averageCount = 0
currentGradientAvg = 0
while True:
    average = 0
    count = 0    
    while count < 9:
        average = average + analogRead()
        count = count + 1
        time.sleep(0.01)
    currentGradient = int(average / 10)
    currentGradientAvg = currentGradientAvg + currentGradient
    averageCount = averageCount + 1
    if averageCount > 9:
        currentGradient = int(currentGradientAvg / 10)
        averageCount = 0
        currentGradientAvg = 0
        getCurrentGradient(currentGradient)    
