#! /usr/bin/python
# Solar Bar, color control sliders
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, commands, subprocess, re, json, sys, os, memcache, numpy
from PIL import Image
from neopixel import *
import includes.data as data
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

# LED strip configuration:import settings as settings
LED_COUNT      = 432     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 20    # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

############################################
######## YOU HAVE TO RUN AS ROOT!
############################################

def hexToRGB(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

# setup the strip
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, ws.WS2811_STRIP_GRB)
strip.begin()

for i in range(0, LED_COUNT):
    strip.setPixelColor(i, Color(0, 0, 0))
strip.show()

im = Image.open('gradients/6.png')
imagePixels = list(im.getdata())

imageLocation = 96249
for i in range(0, 144):
    r,g,b,a = imagePixels[imageLocation]
    strip.setPixelColor(i, Color(r,g,b))
    imageLocation = imageLocation - 668
    
imageLocation = 96249
for i in range(288, 145, -1):
    r,g,b,a = imagePixels[imageLocation]
    strip.setPixelColor(i, Color(r,g,b))
    imageLocation = imageLocation - 668
    
imageLocation = 96249
for i in range(289, 432):
    r,g,b,a = imagePixels[imageLocation]
    strip.setPixelColor(i, Color(r,g,b))
    imageLocation = imageLocation - 668
    
strip.show()




