


from datetime import timedelta, datetime, tzinfo, time
import random
import re

__author__ = 'Hongyu Su'
__version__= '0.1'



def get_site(city):
  res = {'a':1,'b':2,'c':2,'b1':2,'c1':3,'b2':3,'c2':3,'c11':3,'b21':3,'c21':3,'c12':3,'b22':3,'c22':3,'c13':3,'b32':3,'c32':3,'av':1,'bv':2,'cv':2,'b1v':2,'cv1':3,'bv2':3}
  return res


def find_sites(trips):
  '''
  fill in trip information
  '''
  res = []
  tripsLen = len(trips)
  for i in xrange(tripsLen-1):
    city      = trips[i]['endCity']
    siteInfo  = get_site(city)
    startTime = trips[i]['endTime']
    endTime   = trips[i+1]['startTime']
    startTime = datetime(int(startTime.split(' ')[0].split('-')[0]),int(startTime.split(' ')[0].split('-')[1]),int(startTime.split(' ')[0].split('-')[2]),int(startTime.split(' ')[1].split(':')[0]),int(startTime.split(' ')[1].split(':')[1]))
    endTime = datetime(int(endTime.split(' ')[0].split('-')[0]),int(endTime.split(' ')[0].split('-')[1]),int(endTime.split(' ')[0].split('-')[2]),int(endTime.split(' ')[1].split(':')[0]),int(endTime.split(' ')[1].split(':')[1]))
    
    while startTime < endTime and len(siteInfo.keys())>0:
      if startTime.time() < time(8,0):
        startTime = datetime(startTime.year,startTime.month,startTime.day,8,0,0)
      elif startTime.time() >= time(18,0):
        startTime = datetime(startTime.year,startTime.month,startTime.day+1,8,0,0)
      else:
        # pick a site
        key = siteInfo.keys()[0]
        tmpres = {}
        tmpres["type"] = "site"
        tmpres["popularity"] = random.randrange(1,5,1)
        tmpres["City"] = city
        tmpres["name"] = key
        tmpres["price"] =  random.randrange(10,50,5)
        tmpres["startTime"] = re.sub('T',' ',startTime.isoformat())
        tmpres["duration"] = siteInfo[key] 
        startTime += timedelta(hours=siteInfo[key])
        if startTime.time() > time(18,0): startTime = datetime(startTime.year,startTime.month,startTime.day,18,0,0)
        tmpres["endTime"] = re.sub('T',' ',startTime.isoformat())
        del siteInfo[key]
        res.append(tmpres)
  return res





