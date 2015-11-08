


from datetime import timedelta, datetime, tzinfo, time
import random
import re
from getSights import getSightsByCity
import json
import operator

__author__ = 'Hongyu Su'
__version__= '0.1'




def get_site(city):
  siteInfo = getSightsByCity(city)
  tmpres = {}
  for i in range(len(siteInfo)):
    tmpres[i] = siteInfo[i]['popularity']
  tmpres = sorted(tmpres.items(), key=operator.itemgetter(1))
  tmpres.reverse()
  newsiteInfo = []
  for key,val in tmpres:
    newsiteInfo.append((siteInfo[key]['name'],val))
  siteInfo = newsiteInfo
  newsiteInfo=[]
  tmpres = {}
  return siteInfo


def find_restaurants(trips):
  '''
  fill in trip information
  '''
  res = []
  restIndex = 0
  tripsLen = len(trips)
  for i in xrange(tripsLen-1):
    city      = trips[i]['endCityName']
    siteInfo  = get_site(city)
    startTime = trips[i]['endTime']
    endTime   = trips[i+1]['startTime']
    startTime = datetime(int(startTime.split(' ')[0].split('-')[0]),int(startTime.split(' ')[0].split('-')[1]),int(startTime.split(' ')[0].split('-')[2]),int(startTime.split(' ')[1].split(':')[0]),int(startTime.split(' ')[1].split(':')[1]))
    endTime = datetime(int(endTime.split(' ')[0].split('-')[0]),int(endTime.split(' ')[0].split('-')[1]),int(endTime.split(' ')[0].split('-')[2]),int(endTime.split(' ')[1].split(':')[0]),int(endTime.split(' ')[1].split(':')[1]))
    
    while startTime < endTime and len(siteInfo)>restIndex:
      st1 = datetime(startTime.year,startTime.month,startTime.day,19,startTime.minute,startTime.second)
      st2 = datetime(startTime.year,startTime.month,startTime.day,21,startTime.minute,startTime.second)
      if st1>=startTime and st2<=endTime:
        name,popularity = siteInfo[restIndex]
        restIndex+=1
        tmpres = {}
        tmpres["type"] = "restaurant"
        tmpres["popularity"] = popularity
        tmpres["City"] = city
        tmpres["name"] = name
        tmpres["price"] =  random.randrange(10,50,5)
        tmpres["startTime"] = re.sub('T',' ',st1.isoformat())
        tmpres["duration"] = 3
        tmpres["endTime"] = re.sub('T',' ',st2.isoformat())
        startTime = datetime(startTime.year,startTime.month,startTime.day+1,8,startTime.minute,startTime.second)
        res.append(tmpres)
      else:
        break
  return res





