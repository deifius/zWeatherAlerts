#!/usr/bin/env python3

from weatheralerts import WeatherAlerts
import json, sys, select, os, pdb, datetime
from time import sleep
from math import sqrt

"""weatheralerts is throwing errors,
I've found noaa provided rest interface:
https://alerts.weather.gov/cap/co.php?x=0
https://alerts.weather.gov/cap/wwaatmget.php?x=MIC055&y=0
ForecastZones can be k-nearest neighbored from ForecastZoneGeoLoc.txt
"""

def eat_Forecast_Zones():
	with open('ForecastZoneGeoLoc.txt') as stuff:  stats = stuff.read().split('\n')
	for each_stat in enumerate(stats):
		stats[each_stat[0]] = each_stat[1].split('|')
	while stats[-1] == [""]: stats.pop()
	return stats

def euclid_distance(point1, point2):
	try: return sqrt((float(point1[0])-float(point2[0]))**2+(float(point1[1])-float(point2[1]))**2)
	except: print(f'points not formatted correctly?')

def k_nearest_neighbor(locationA, fc_zone_stats, k):
	distances = [[euclid_distance(locationA, that[-2:])]+that for that in fc_zone_stats]
	distances.sort()
	return distances[0:k]

def convert_forecast_zone_to_URL(stat_entry):
	code = f'{stat_entry[1]}C{stat_entry[7][2:]}'
	return f'https://alerts.weather.gov/cap/wwaatmget.php?x={code}&y=0  > forecasts/{code}'

def pull_noaa_alerts_by_forecast_zone(location, k):
	this = k_nearest_neighbor(location, eat_Forecast_Zones(), k)
	for each in this:
		os.system(f'curl {convert_forecast_zone_to_URL(each)}')

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
