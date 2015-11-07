


import json
import urllib


__author__ = 'Hongyu Su'
__version__ = '0.1' 



def launch_API(departureAirport, arrivalAirport, departureTime, arrivalTime):
  '''
  Input: departure city, arrivial city, departure time, arrivial time
  Output: flight information 
  >>>launch_API('HEL','LHR','20151201000000','20151202000000')
  '''
  s = 'https://slush.ecom.finnair.com/api/getTimeTable?departureAirport='
  s += departureAirport
  s += '&arrivalAirport='
  s += arrivalAirport
  s += '&departureTime='
  s += departureTime
  s += '&arrivalTime='
  s += arrivalTime
  s += ''
  j=urllib.urlopen(s)
  data = json.load(j)
  pass


if __name__ == '__main__':
  print launch_API('HEL','LHR','20151201000000','20151202000000')
  pass