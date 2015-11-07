
import json
import urllib
from pprint import pprint
import random
import string

__author__ = 'Hongyu Su'
__version__ = '0.1' 

def launch_API_tmp(departureAirport, arrivalAirport, departureTime, arrivalTime):
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
  data = json.loads(re.sub('\\"','"',response).decode('utf8'))
  print type(data)
  pass

def formatDateTime(inputString):
  return inputString[0:4] +'-'+ inputString[4:6] + '-'+inputString[6:8] +' '+ inputString[8:10]+ ':'+inputString[10:12]+':'+ inputString[12:14]

def formatTime(inputString):
  return inputString[0:2] +':'+ inputString[2:4] + ':'+inputString[4:6]

def launch_API(departureAirport, arrivalAirport, departureTime, arrivalTime):
  '''
  Input: departure city, arrivial city, departure time, arrivial time
  Output: flight information, HEL, LHR
  >>>launch_API('HEL','LHR','20151201000000','20151202000000')
  ('HEL', 'LHR', '2015-12-01 08:02:00', '2015-12-01 12:48:00', 'AY9702', '360.10', '04:46:00')
  '''
  random.seed(departureAirport + arrivalAirport + departureTime+arrivalTime)
  arrivalTime = str(eval(departureTime) )
  chars = string.ascii_uppercase + string.digits
  size = 7
  flightCode = 'AY' + ''.join(random.choice(string.digits) for _ in range(4))
  ticketPrice = '%.2f' % (random.randrange(100,400,10)+random.randrange(0,10,1)/float(10))
  departureTime  = str(eval(departureTime) + random.randrange(8,12,1)*10000 + random.randrange(0,30,1)*100)
  arrivalTime  = str(eval(arrivalTime) + random.randrange(12,16,1)*10000 + random.randrange(31,60,1)*100)
  duration = "%06d" % (eval(arrivalTime)-eval(departureTime))
  return (departureAirport,arrivalAirport,formatDateTime(departureTime),formatDateTime(arrivalTime),flightCode,ticketPrice,formatTime(duration))
  pass


if __name__ == '__main__':
  print launch_API('HEL','LHR','20151201000000','20151202000000')
  pass