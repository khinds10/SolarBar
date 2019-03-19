#! /usr/bin/python
# Solar Bar, color strip controller
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, commands, subprocess, re, json, sys, os, memcache, numpy
from PIL import Image
from neopixel import *
import includes.data as data
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

# LED strip configuration:import settings as settings
LED_COUNT       = 288    # Number of LED pixels.
#LED_COUNT        = 512
LED_STRIP_COUNT = 3       # How many strips are there total for the number of pixels
LED_PIN         = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ     = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA         = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS  = 200      # Set to 0 for darkest and 255 for brightest
LED_INVERT      = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL     = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

##################################################
######## YOU HAVE TO RUN AS ROOT!
##################################################
# setup the strip
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, ws.WS2811_STRIP_GRB)
strip.begin()

# turn all lights off to start
for i in range(0, LED_COUNT):
    strip.setPixelColor(i, Color(0, 0, 0))
strip.show()

def illuminate():
    global currentImage
    currentPixel = 0
    evenNumberedStrip = False
    for currentStrip in range(0, LED_COUNT, (LED_COUNT/LED_STRIP_COUNT)):
        currentPixel = 0
        if evenNumberedStrip:
            for ledLight in range(currentStrip, currentStrip + (LED_COUNT/LED_STRIP_COUNT), 1):
                r,g,b,a = currentImage[currentPixel]
                strip.setPixelColor(ledLight, Color(r,g,b))
                currentPixel = currentPixel + 1
        else:
            for ledLight in range(currentStrip + (LED_COUNT/LED_STRIP_COUNT), currentStrip, -1):
                r,g,b,a = currentImage[currentPixel]
                strip.setPixelColor(ledLight, Color(r,g,b))
                currentPixel = currentPixel + 1

        # the LED strips are upside down, right side up sequentially on the device, so we must iterate through back and forth the LEDs
        evenNumberedStrip = not evenNumberedStrip       
    strip.show()

def shiftGradient():
    global currentSunrisePosition, currentImage
    if currentSunrisePosition > (height - 1):
        currentSunrisePosition = height - 1        
    currentImage = imagePixels[currentSunrisePosition:currentSunrisePosition + (LED_COUNT/LED_STRIP_COUNT)]

im = Image.open('gradients/3.png')
imagePixels = list(im.getdata())
width, height = im.size
ledStripCount = LED_COUNT / LED_STRIP_COUNT
currentSunrisePosition = 0

# the sun color is always at the bottom and can 'consume' more and more of the current gradient
sunColor = imagePixels[-1]

# cut one line out of the image and pad it with the "full sun color" at the bottom
completeGradient = []
for i in range(0, (width * height) * 2, width):
    if i < (width * height):
        completeGradient.append(imagePixels[i])
    else:
        completeGradient.append(sunColor)
imagePixels = completeGradient

# get current gradient as is to be manipulated, original image 
#   that the completeGradient can slowly take over as the "sun rises" or control panel adjusted
currentImage = imagePixels[0:(LED_COUNT/LED_STRIP_COUNT)]

# start waiting on any changes to the gradient to adjust the LED strips as necessary
currentSunrisePosition = 0
gradientCheck = 0
while True:
    #gradientCheck = mc.get("GRADIENT")    
    gradientCheck = gradientCheck + 1
    
    if gradientCheck > height * 2:
        gradientCheck = 1
    
    # we have a gradient position incoming, consume and adjust light illumination as instructed
    if gradientCheck:  
        currentSunrisePosition = int(gradientCheck)
        shiftGradient()
        illuminate()

    # wait and go around again
    mc.set("GRADIENT", "")
