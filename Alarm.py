#! /usr/bin/python
# Solar Bar, alarm manager
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, commands, subprocess, re, json, sys, os, memcache, json, datetime
import includes.data as data

#-------------------------------------------------------------------------------------------------------------
# cronjob runs this script at 4am sleep till alarm set time, then start the sunrise gradient illumination
#-------------------------------------------------------------------------------------------------------------

isAlarmSet = data.getJSONFromDataFile("./data/alarmSet.data")
alarmTime = data.getJSONFromDataFile("./data/alarm.data")

timeNow = datetime.datetime.now()
print time.now()
alarmTimestampString = str(timeNow.month) + "/" + str(timeNow.day) + "/" + str(timeNow.year) + "/" + str(alarmTime[0]) + "/" + str(alarmTime[1])
alarmTimestamp = time.mktime(datetime.datetime.strptime(alarmTimestampString, "%m/%d/%Y/%H/%M").timetuple())

if isAlarmSet == "True":
    print isAlarmSet
    print 

    timeTillSunrise = alarmTimestamp - timeNow
    if (timeTillSunrise > 0):
        print "Sleeping till Alarm is set (zzz): " + str(timeTillSunrise) + " seconds"
        time.sleep(timeTillSunrise)
