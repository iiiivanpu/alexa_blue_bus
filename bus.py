#from selenium import webdriver
from pyquery import PyQuery as pq
import re
import requests

def on_start():
	stop = input("Enter your bus stop: ")
	url = "https://ltp.umich.edu/transit/BB.php"
	resp = requests.get(url)
	doc = pq(resp.text)
	for item in doc.find('.main table').eq(1).find('tr').items():
		if item.find("td").eq(1).text() == stop:
			url = item.find("a").attr("href")
			break
	
	doc = pq(requests.get(url).text)
	# for each in doc.find(".r2").items():
	# 	print(each)
	print(doc.find(".r2").eq(0).find('td').eq(1).text())

on_start()

# stop_num = {
    #     'Baits I' : '411',
	# 	'Baits II Inbound' : '409',
	# 	'Bursley Hall Inbound' : '407',
	# 	'Pierpont Commons, Murfin Inbound' : '551',
	# 	'Fuller Rd at Lot NC-78, Mitchell Field' : '450',
	# 	'Glen/Catherine Inbound' : '310',
	# 	'Rackham Bldg' : '211',
	# 	'Central Campus Transit Center: Chemistry' : '250',
	# 	'Stockwell Hall Outbound' : '301',
	# 	'Cardiovascular Center' : '303',
	# 	'Zina Pitcher' : '306',
	# 	'Glen/Catherine Outbound' : '309',
	# 	'Fuller Rd at Mitchell Field, Lot M-75' : '350',
	# 	'Pierpont Commons, Murfin Outbound' : '550',
	# 	'Bursley Hall Outbound' : '408',
	# 	'Baits II Outbound' : '410',
	# 	'Baits I' : '411'
    # }
	# url = 'http://ltp.umich.edu/stops/?s=N' + stop_num[stop] 
	# print(url)