import itertools
import json
from datetime import datetime, timedelta
from hotels import find_hotels
from sites import find_sites

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

def stayTime(city):
    """
    Parameters:
    -----------
    city: String, city name

    Returns:
    --------
    Int, the number of days to stay
    """
    return 3
    
def callSu(startcity, endcity, flydate):
    takeoftime = flydate.strftime("%Y%m%d%H%M%S")
    landtime = (flydate + timedelta(0,3600*23+3599)).strftime("%Y%m%d%H%M%S")
    return startcity, endcity, takeoftime, landtime

def eval(citys, cityCode, start, end, extradays):
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
        trip["startTime"] = starttime
        trip["endTime"] = endtime
        trip["FLN"] = flightnumber
        trip["price"] = price
        totalprice += float(price)
        trips.append(trip)

        stay = stayTime(citys[i+1])
        if extradays > 0:
            pad = round(extradays/float(ncity))
            stay += pad
            extradays -= pad
            ncity -= 1
        elif extradays < 0:
            pad = round(abs(extradays)/float(ncity))
            stay -= pad
            extradays += pad
            ncity -= 1            
        flytime = timedelta(stay) + flytime

    #query hotels and sites
    hotels = find_hotels(trips)
    sites = find_sites(trips)
    trips.extend(hotels)
    trips.extend(sites)
    print '>>>>>>'

    opt = {}
    opt["totalPrice"] = "%.2f" % totalprice
    opt["trips"] = trips
    return opt

def findThem(homeCity, citys, startTime, endTime):
    cityCode = readCityCode()

    staytimes = [stayTime(city) for city in citys]
    needdays = sum(staytimes)

    y1,m1,d1 = map(int, startTime.split('-'))
    start = datetime(y1, m1, d1)
    y2,m2,d2 = map(int, endTime.split('-'))
    end = datetime(y2, m2, d2)
    days = (end - start).days

    extradays = days - needdays
    options = itertools.permutations(citys)
    costs = []
    allOptions = []
    for candidate in options:
        visitOrder = [homeCity] + list(candidate) + [homeCity]
        opt = eval(visitOrder, cityCode, start, end, extradays)
        costs.append(float(opt["totalPrice"]))
        allOptions.append(opt)

    # Sort by prices
    inds = sorted(range(len(costs)), key=lambda k: costs[k])    
    sortedOptions = [allOptions[ind] for ind in inds]
    result = {}
    result["options"] = sortedOptions
    return json.dumps(result)

if __name__ == "__main__":
    a = findThem("Helsinki", ["Paris", "Rome"], "2015-11-01","2015-11-07")
    print a
    raw_input()
    b = findThem("Helsinki", ["Munich", "Milan", "Berlin"], "2015-12-01","2015-12-15")
    print b
