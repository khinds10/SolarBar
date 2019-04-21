#! /usr/bin/python
# Solar Bar, color control sliders
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, json, commands, subprocess, re, json, sys, os, memcache
import includes.data as data
import RPi.GPIO as GPIO
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

# adjustable slider, so be it. you shall be the fellowship of the lamp
# http://razzpisampler.oreilly.com/ch08.html
GPIO.setmode(GPIO.BCM)
a_pin = 24
b_pin = 23

def discharge():
    """discharge the pin to start counting how long it takes to recharge"""
    GPIO.setup(a_pin, GPIO.IN)
    GPIO.setup(b_pin, GPIO.OUT)
    GPIO.output(b_pin, False)
    time.sleep(0.005)

def chargeTime():
    """arbitrary counter for how it takes to charge again"""
    GPIO.setup(b_pin, GPIO.IN)
    GPIO.setup(a_pin, GPIO.OUT)
    count = 0
    GPIO.output(a_pin, True)
    while not GPIO.input(b_pin):
        count += 1
    return count

def analogRead():
    """read in the arbitrary 'charge time' counter"""
    discharge()
    return chargeTime()

# begin loop over the analog read of the slider position 
#   to set the gradient position desired for the LED strip
averageCount, currentGradientAvg = 0, 0
currentSliderPosition, newSliderPosition = 0,0
while True:
    try:
        average, count = 0, 0
        while count < 9:
            average += analogRead()
            count += 1
            time.sleep(0.01)
        currentGradientAvg += int(average / 10)
        averageCount += 1
    
        # save the new average slider reading, making sure it's out of the current range +/- 24 (this reduces noisy readings)
        if averageCount > 9:
            newSliderPosition = int(currentGradientAvg / 10)
            if (newSliderPosition > currentSliderPosition + 5) or (newSliderPosition < currentSliderPosition - 5):
                currentSliderPosition = newSliderPosition
                data.saveSliderPosition(currentSliderPosition)
                print currentSliderPosition
            averageCount, currentGradientAvg = 0, 0 
    except (Exception):
        time.sleep(0.1)
