import requests
import json
from urllib.request import urlopen

url="http://ip-api.com/json/"

response = urlopen(url)
response=response.read()
data=json.loads(response)

def getIP():
    return ((str)(data['query']))

def continent():
    return((str)(data['continent']))

def continentCode():
    return((str)(data['continentCode']))

def country():
    return((str)(data['country']))

def countryCode():
    return((str)(data['countryCode']))

def region():
    return((str)(data['regionName']))

def regionCode():
    return((str)(data['region']))

def city():
    return((str)(data['city']))

def zip():
    return((str)(data['zip']))

def latitude():
    return((str)(data['lat']))

def longitude():
    return((str)(data['lon']))

def timezone():
    return((str)(data['timezone']))

def offset():
    return((str)(data['offset']))

def currencyCode():
    return((str)(data['currency']))

def isp():
    return((str)(data['isp']))

def org():
    return((str)(data['org']))

def asname():
    return((str)(data['as']))

def info():
    return((str)("Developed by Aditya Khemka from India"))

def debug():
    print("Please check if you have a stable internet connection")
    print("You cannot call this for more than 45 times a minute")
    print("your current IP address is used by default. To change IP address, call the setIP function")
    print("It is possible that ip-api (open source service used to gather data) is not serving a particular request in your region")
    return("")
