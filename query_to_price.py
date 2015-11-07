
import json
import urllib
from pprint import pprint
import codecs
import re

__author__ = 'Hongyu Su'
__version__ = '0.1' 

def launch_API(departureAirport, arrivalAirport, departureTime, arrivalTime):
  '''
  Input: departure city, arrivial city, departure time, arrivial time
  Output: flight information, HEL, LHR
  >>>launch_API('HEL','LHR','20151201000000','20151202000000')
  '''
  url = 'https://slush:f1na350!@slush.ecom.finnair.com/api/getTimeTable?departureAirport='
  url += departureAirport
  url += '&arrivalAirport='
  url += arrivalAirport
  url += '&departureTime='
  url += departureTime
  url += '&arrivalTime='
  url += arrivalTime
  url += ''


  response = urllib.urlopen(url).read()
  open('tmp','w').write(re.sub('.*','',response))

  

  pass


if __name__ == '__main__':
  launch_API('HEL','LHR','20151201000000','20151202000000')
  pass