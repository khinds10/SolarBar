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
alarmTimestamp = time.mktime(datetime.strptime.datetime(str(timeNow.month) + "/" + str(timeNow.day) + "/" + str(timeNow.year) + "/" + str(alarmTime[0]) + "/" + str(alarmTime[1])), "%m/%d/%Y/%H/%M").timetuple())
if isAlarmSet == "True":
    timeTillAlarm = alarmTimestamp - time.time()
    if (timeTillAlarm > 0):
        print "Sleeping till Alarm is set (zzz): " + str(timeTillAlarm) + " seconds"
        time.sleep(timeTillAlarm)
