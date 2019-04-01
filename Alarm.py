#! /usr/bin/python
# Solar Bar, alarm manager
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, commands, subprocess, re, json, sys, os, memcache, json, datetime
import includes.data as data

#-------------------------------------------------------------------------------------------------------------
# cronjob runs this script at 4am sleep till alarm set time, then start the sunrise gradient illumination
#-------------------------------------------------------------------------------------------------------------

def percentage(part, whole):
  return 100 * float(part)/float(whole)

# get the upcoming timestamp for when the alarm is set for today
isAlarmSet = data.getJSONFromDataFile("/home/pi/SolarBar/data/alarmSet.data")
alarmTime = data.getJSONFromDataFile("/home/pi/SolarBar/data/alarm.data")
timeNow = datetime.datetime.now()
timeStruct = (timeNow.year, timeNow.month, timeNow.day, alarmTime[0], alarmTime[1], timeNow.second, datetime.datetime.now().timetuple().tm_wday, datetime.datetime.now().timetuple().tm_yday, datetime.datetime.now().timetuple().tm_isdst)
alarmTimestamp = time.mktime(timeStruct)

# how long the alarm will run for
seconds = 60*1

# if the alarm is set, then begin the sunrise at the designated time
if isAlarmSet == "True":
    timeTillAlarm = alarmTimestamp - time.time()
    if (timeTillAlarm > 0):
        print "Sleeping till Alarm is set (zzz): " + str(timeTillAlarm) + " seconds"
        time.sleep(timeTillAlarm)
        
        # alarm is ringing, begin the gradient
        print "Alarm is ringing"
        second = 0
        percent = 0
        data.saveLightOn('1')
        data.saveSliderPosition('0')
        while second < seconds:
            second = second + 1
            percent = int(percentage(second, seconds))
            print "Sun is " + str(percent) + "% risen"
            data.saveSliderPosition(str(percent * 5))
            time.sleep(1)

        # wait another cycle of the seconds passing then turn off the light
        time.sleep(seconds)
        data.saveLightOn('0')
