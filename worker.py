import itertools
import json
import random
import sys
import math
from datetime import datetime, timedelta
from hotels import find_hotels
from sites import find_sites
from restaurants import find_restaurants
import random
from query_to_price import launch_API

def readCityCode():
    cityCode = {}
    lines = open("cityCodes.txt").read().split("\n")
    for line in lines:
        if not line:
            continue
        words = line.split()
        code, name  = words[0], words[1]
        cityCode[name] = code
    return cityCode


    
def callSu(startcity, endcity, flydate):
    takeoftime = flydate.strftime("%Y%m%d%H%M%S")
    landtime = (flydate + timedelta(0,3600*23+3599)).strftime("%Y%m%d%H%M%S")
    return startcity, endcity, takeoftime, landtime

def eval(citys, cityCode, start, end, extradays, needdays, STAYTIME):
    """
    For one options of visiting orders of the citys,
    return the total price and flying plan


    Parameters:
    ----------


    Returns:
    --------
    """

    n = len(citys)
    flytime = start
    totalprice = 0
    ncity = n -2
    trips = []

    for i in xrange(n-1):
        # get the one flight info
        startcity = cityCode[citys[i]]
        endcity = cityCode[citys[i+1]]
        a,b,c,d = callSu(startcity, endcity, flytime)
        startAirport, endAirport, starttime, endtime, flightnumber, price, duration = launch_API(a,b,c,d)

        trip = {}
        trip["type"] = 'flight'
        trip["startCity"] = startAirport
        trip["endCity"] = endAirport
        trip["startCityName"] = citys[i]
        trip["endCityName"] = citys[i+1]
        trip["startTime"] = starttime
        trip["endTime"] = endtime
        trip["FLN"] = flightnumber
        trip["price"] = price
        totalprice += float(price)
        trips.append(trip)

        extradays_copy = extradays
        stay = STAYTIME[citys[i+1]]
        if extradays > 0:
            pad = round(abs(extradays)/float(ncity))
            #pad = round(abs(stay)/float(needdays)*abs(extradays_copy))
            #pad = 1
            stay += pad
            extradays -= pad
            ncity -= 1
        elif extradays < 0:
            #pad = math.ceil(abs(stay)/float(needdays)*abs(extradays_copy))
            #pad = 1
            pad = round(abs(extradays)/float(ncity))
            stay -= pad
            extradays += pad
            ncity -= 1     
        flytime = timedelta(stay) + flytime

    #query hotels and sites
    hotels = find_hotels(trips)
    sites = find_sites(trips)
    rests = find_restaurants(trips)
    trips.extend(hotels)
    trips.extend(sites)
    trips.extend(rests)

    opt = {}
    opt["totalPrice"] = "%.2f" % totalprice
    opt["trips"] = trips
    return opt

def readTime():
    lines = open("visit_time.txt").read().split("\n")
    time = {}
    for line in lines:
        if not line:
            continue
        name, t = line.split(" ")
        time[name] = int(t)
    return time

def findThem(homeCity, citys, startTime, endTime):
    cityCode = readCityCode()

    stayTime = readTime()
    staytimes = [stayTime[city] for city in citys]
    
    needdays = sum(staytimes)

    y1,m1,d1 = map(int, startTime.split('-'))
    start = datetime(y1, m1, d1)
    y2,m2,d2 = map(int, endTime.split('-'))
    end = datetime(y2, m2, d2)
    days = (end - start).days

    extradays = days - needdays

    while abs(extradays) >= len(citys) and extradays < 0:
        minind = staytimes.index(min(staytimes))
        del citys[minind]
        staytimes = [stayTime[city] for city in citys]
        needdays = sum(staytimes)
        extradays = days - needdays        


    options = itertools.permutations(citys)
    costs = []
    allOptions = []
    
    for candidate in options:
        visitOrder = [homeCity] + list(candidate) + [homeCity]
        opt = eval(visitOrder, cityCode, start, end, extradays, needdays, stayTime)
        costs.append(float(opt["totalPrice"]))
        allOptions.append(opt)

    # Sort by prices
    inds = sorted(range(len(costs)), key=lambda k: costs[k])    
    sortedOptions = [allOptions[ind] for ind in inds[0:5]]
    result = {}
    result["options"] = sortedOptions
    return json.dumps(result)

if __name__ == "__main__":

    #a = findThem("Helsinki", ["Paris", "Rome"], "2015-11-01","2015-11-07")
    #print a
    #c = findThem("Helsinki", ["Rome", "Barcelona", "Paris"], "2015-10-01","2015-10-07")
    #print c
    c = findThem("Helsinki", ["Munich", "Milan", "Berlin"], "2015-12-01","2015-12-15")
    print c

