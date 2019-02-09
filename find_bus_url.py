import requests as req
from pyquery import PyQuery as pq 

def find_bus_url(stop_name):
    url = "https://ltp.umich.edu/transit/BB.php"
    resp = req.get(url)
    doc = pq(resp.text)
    for item in doc.find('.main table').eq(1).find('tr').items():
        if item.find("td").eq(1).text() == stop_name:
            return item.find("a").attr("href")

print(find_bus_url("Baits I"))