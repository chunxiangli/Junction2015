


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


def find_sites(trips):
  '''
  fill in trip information
  '''
  
  res = []
  siteIndex = 0
  tripsLen = len(trips)
  for i in xrange(tripsLen-1):
    city      = trips[i]['endCityName']
    siteInfo  = get_site(city)
    startTime = trips[i]['endTime']
    endTime   = trips[i+1]['startTime']
    startTime = datetime(int(startTime.split(' ')[0].split('-')[0]),int(startTime.split(' ')[0].split('-')[1]),int(startTime.split(' ')[0].split('-')[2]),int(startTime.split(' ')[1].split(':')[0]),int(startTime.split(' ')[1].split(':')[1]))
    endTime = datetime(int(endTime.split(' ')[0].split('-')[0]),int(endTime.split(' ')[0].split('-')[1]),int(endTime.split(' ')[0].split('-')[2]),int(endTime.split(' ')[1].split(':')[0]),int(endTime.split(' ')[1].split(':')[1]))
    
    while startTime < endTime:
      if startTime.time() < time(8,0):
        startTime = datetime(startTime.year,startTime.month,startTime.day,8,0,0)
      elif startTime.time() >= time(18,0):
        startTime = datetime(startTime.year,startTime.month,startTime.day+1,8,0,0)
      else:
        # pick a site
        name,popularity = siteInfo[siteIndex]
        siteIndex += 1
        if len(siteInfo)<=siteIndex: siteIndex =0
        tmpres = {}
        tmpres["type"] = "site"
        tmpres["popularity"] = popularity
        tmpres["City"] = city
        tmpres["name"] = name
        tmpres["price"] =  random.randrange(10,50,5)
        tmpres["startTime"] = re.sub('T',' ',startTime.isoformat())
        tmpres["duration"] = random.randrange(1,3,1) 
        startTime += timedelta(hours=tmpres["duration"])
        startTime -= timedelta(minutes=10)
        if startTime.time() > time(18,0): startTime = datetime(startTime.year,startTime.month,startTime.day,18,0,0)
        tmpres["endTime"] = re.sub('T',' ',startTime.isoformat())
        res.append(tmpres)
  return res





