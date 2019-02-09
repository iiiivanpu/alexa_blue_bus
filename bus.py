#from selenium import webdriver
from pyquery import PyQuery as pq
from flask_ask import Ask, context
from datetime import datetime
from datetime import timedelta  
import re
import requests
import json

def on_start():
	stop = input("Enter your bus stop: ")
	url = "https://ltp.umich.edu/transit/BB.php"
	resp = requests.get(url)
	doc = pq(resp.text)
	for item in doc.find('.main table').eq(1).find('tr').items():
		if item.find("td").eq(1).text() == stop:
			print(stop)
			url = item.find("a").attr("href")
			break
	stop = "+".join(stop.split())
	#location = '1770+Broadway+Street'
	location = '+'.join(get_alexa_location().split())
	doc = pq(requests.get(url).text)
	url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='+ location + '&destinations='
	url += stop + '&mode=walking&key=AIzaSyBRJAYtJKPN0oRlWSz0dYOtB_OBEfcXi8I'
	print(url)
	data = requests.get(url).json()
	
	travel_time = round(data['rows'][0]['elements'][0]['duration']['value']/60)
	
	next_time = re.search('([0-9]*):([0-9]*) ([ap]).m', doc.find(".r2").eq(0).find('td').eq(1).text())
	hour = int(next_time.group(1)) if next_time.group(3) == 'a' else int(next_time.group(1)) + 12
	minutes = int(next_time.group(2)) + travel_time
	
	if datetime.now().hour*60 + datetime.now().minute + travel_time < hour * 60 + minutes:
		print("Can catch")
		print(travel_time)
		print([hour, minutes])
	else:
		print("Can't catch")
		second_bus = re.search('([0-9]*):([0-9]*) ([ap]).m', doc.find(".r2").eq(0).find('td').eq(2).text())
		print(second_bus.group(0), second_bus.group(1))
	

def get_alexa_location():
	return "1770 Broadway Street"
	URL =  "https://api.amazonalexa.com/v1/devices/{}/settings" \
			"/address".format(context.System.device.deviceId)
	TOKEN =  context.System.user.permissions.consentToken
	HEADER = {'Accept': 'application/json',
				'Authorization': 'Bearer {}'.format(TOKEN)}
	r = requests.get(URL, headers=HEADER)
	
	if r.status_code == 200:
		return(r.json()["addressLine1"])
	else:
		return "Invalid request"

on_start()