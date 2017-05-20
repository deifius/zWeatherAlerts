#!/usr/bin/env python3

from weatheralerts import WeatherAlerts
import json, talkey, sys, select, os
from time import sleep


def WeatherIsBad(currentAlerts):
    # festvox or soundfile
    # method for ACKING, like press 1 or some such
    tts = talkey.Talkey()
    while True:
        os.system('clear')
        for eachalert in currentAlerts:
            print(eachalert.split('issued')[0])
            tts.say(eachalert.split('issued')[0])
        print('Hit enter to acknowledge')
        tts.say('Hit enter to acknowledge')
        if sys.stdin in select.select([sys.stdin],[],[],0)[0]:
            line = input()
            break
    sleep(1800)


def checkTheWeather():
    # read samecodes every time and grab any alerts from NOAA
    # if weather is bad and unACKED call ifWeatherIsBad
    whereAmI = json.loads(open('samecodes.txt').read())
    NOAAalerts = WeatherAlerts(samecodes=whereAmI['samecode'])
    print('Checking in with ' + whereAmI['name'])
    allAlerts = []
    for alert in NOAAalerts.alerts:
        allAlerts.append(alert.title)
    return allAlerts

while True:
    currentAlerts = checkTheWeather()
    if currentAlerts != []: WeatherIsBad(currentAlerts)
    else: print('all OK!')
    sleep(300)
