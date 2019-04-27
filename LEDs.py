#! /usr/bin/python
# Solar Bar, color strip controller
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, commands, subprocess, re, json, sys, os, memcache, numpy
from PIL import Image
from neopixel import *
import includes.data as data

# LED strip configuration:import settings as settings
LED_COUNT       = 576     # Number of LED pixels.
LED_STRIP_COUNT = 4       # How many strips are there total for the number of pixels
LED_PIN         = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ     = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA         = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS  = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT      = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL     = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_TOTAL_STRIPS = LED_COUNT/LED_STRIP_COUNT

##################################################
######## YOU HAVE TO RUN AS ROOT!
##################################################

# setup the strip
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, ws.WS2811_STRIP_GRB)
strip.begin()

def reset():
    """turn all lights off RGB = 000"""
    global isIllumniated
    print "reset()"
    for i in range(0, LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))
    isIllumniated = False
    strip.show()

def illuminate():
    """turn on the strip to the current gradient set"""
    global isIllumniated, currentImage
    print "illuminate()"
    currentPixel = 0
    evenNumberedStrip = False
    for currentStrip in range(0, LED_COUNT, (LED_TOTAL_STRIPS)):
        currentPixel = 0
        if evenNumberedStrip:
            for ledLight in range(currentStrip, currentStrip + (LED_TOTAL_STRIPS), 1):
                r,g,b,a = currentImage[currentPixel]
                strip.setPixelColor(ledLight, Color(r,g,b))
                currentPixel = currentPixel + 1
        else:
            for ledLight in range(currentStrip + (LED_TOTAL_STRIPS), currentStrip, -1):
                r,g,b,a = currentImage[currentPixel]
                strip.setPixelColor(ledLight, Color(r,g,b))
                currentPixel = currentPixel + 1

        # the LED strips are upside down, right side up sequentially on the device, so we must iterate through back and forth the LEDs
        evenNumberedStrip = not evenNumberedStrip       
    isIllumniated = True
    strip.show()

def saveDebugImage():
    """save debug image to show what the panel will display"""
    global currentImage
    newImage = Image.new("RGB", (1,len(currentImage)))
    newImage.putdata(currentImage)
    newImage.save('/home/pi/SolarBar/currentPanelColors.png')

def shiftGradient():
    """move the gradient"""
    print "shiftGradient() = " + str(currentSunrisePosition)
    global currentSunrisePosition, currentImage
    if currentSunrisePosition > (imgHeight - 1):
        currentSunrisePosition = imgHeight - 1        
    currentImage = imagePixels[currentSunrisePosition:currentSunrisePosition + (LED_TOTAL_STRIPS)]
    saveDebugImage()
    
def getGradient():
    """get the gradient chosen into memory"""
    global currentImage, imgWidth, imgHeight, imagePixels
    print "getGradient() = " + str(gradientSet)
    im = Image.open('/home/pi/SolarBar/gradients/' + str(gradientSet) + '.png')
    imagePixels = list(im.getdata())
    imgWidth, imgHeight = im.size

    # the sun color is always at the bottom and can 'consume' more and more of the current gradient
    currentSunrisePosition = 0
    sunColor = imagePixels[-1]

    # cut one line out of the image and pad it with the "full sun color" at the bottom
    completeGradient = []
    for i in range(0, (imgWidth * imgHeight) * 2, imgWidth):
        if i < (imgWidth * imgHeight):
            completeGradient.append(imagePixels[i])
        else:
            completeGradient.append(sunColor)
    imagePixels = completeGradient

    # get current gradient as is to be manipulated, original image 
    #   that the completeGradient can slowly take over as the "sun rises" or control panel adjusted
    currentImage = imagePixels[0:(LED_TOTAL_STRIPS)]
    saveDebugImage()

def getCurrentPanelSettings():
    """get the currently set values for what the light panel is supposed to reflect"""
    global gradientSet, lightOn, currentPosition
    gradientSet = data.getJSONFromDataFile('/home/pi/SolarBar/data/gradient.data')
    lightOn = data.getJSONFromDataFile('/home/pi/SolarBar/data/lightOn.data')
    try:
        currentPosition = int(data.getJSONFromDataFile('/home/pi/SolarBar/data/position.data'))
        currentPosition = currentPosition * 5
    except:
        currentPosition = 0
    print "getCurrentPanelSettings() = gradientSet: " + str(gradientSet) + " / lightOn: " + str(lightOn) + " / currentPosition: " + str(currentPosition)

# load current settings for the panel
gradientSet, lightOn, currentPosition, isIllumniated = ["1", "0", "0", False]
prevGradient, prevPosition= ["1", "0"]
imgWidth, imgHeight = [0,0]
imagePixels = None
getCurrentPanelSettings()
reset()
getGradient()

# begin the panel
while True:
    try:
        # light on/off if changed
        if lightOn == "1" and not isIllumniated:
            illuminate()
        if lightOn == "0" and isIllumniated:
            reset()

        # update gradient if new one is set
        if gradientSet != prevGradient:
            getGradient()
            if isIllumniated:
                illuminate()
            prevGradient = gradientSet

        # update 
        if currentPosition != prevPosition:
            currentSunrisePosition = currentPosition
            shiftGradient()
            if isIllumniated:
                illuminate()
            prevPosition = currentPosition

        # go around again
        getCurrentPanelSettings()
        time.sleep(0.1)
    except (Exception):
        time.sleep(0.1)
