#!/usr/bin/env python3

from weatheralerts import WeatherAlerts
import json, sys, select, os, pdb, datetime
from time import sleep


"""weatheralerts is throwing errors,
I've found noaa provided rest interface:
https://alerts.weather.gov/cap/co.php?x=0
https://alerts.weather.gov/cap/wwaatmget.php?x=MIC055&y=0
ForecastZones can be k-nearest neighbored from ForecastZoneGeoLoc.txt
"""



def checkTheWeather(**whereAmI):
	# read samecodes every time and grab any alerts from NOAA
	# if weather is bad and unACKED call ifWeatherIsBad
	print('Checking in with ' + whereAmI['name'])
	NOAAalerts = WeatherAlerts(whereAmI['samecode'])
	allAlerts = []
	for alert in NOAAalerts.alerts:
		allAlerts.append(alert.title)
	return whereAmI

def main():
	while True:
		currentAlerts = checkTheWeather()
		namePlace = json.loads(open('samecodes.txt').read())['name']
		timeNow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
		if currentAlerts != []: WeatherIsBad(currentAlerts)
		else: print('all OK in ' + namePlace + " at " + timeNow)
		sleep(300)

if __name__ == "__main__": main()
