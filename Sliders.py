#! /usr/bin/python
# Solar Bar, color control sliders
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, commands, subprocess, re, json, sys, os, memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

# 3 sliders, so be it. you shall be the fellowship of the ring.
