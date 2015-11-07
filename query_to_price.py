
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


def launch_API(departureAirport, arrivalAirport, departureTime, arrivalTime):
  '''
  Input: departure city, arrivial city, departure time, arrivial time
  Output: flight information, HEL, LHR
  >>>launch_API('HEL','LHR','20151201000000','20151202000000')
  ('HEL', 'LHR', '20151201080200', '20151201143900', '80DI5F', 269, '63700')
  '''
  random.seed(departureAirport + arrivalAirport + departureTime+arrivalTime)
  arrivalTime = str(eval(departureTime) )
  chars = string.ascii_uppercase + string.digits
  size = 7
  flightCode = ''.join(random.choice(chars) for _ in range(6))
  ticketPrice = str(random.randrange(200,500,1))
  departureTime  = str(eval(departureTime) + random.randrange(8,12,1)*10000 + random.randrange(0,30,1)*100)
  arrivalTime  = str(eval(arrivalTime) + random.randrange(12,16,1)*10000 + random.randrange(31,60,1)*100)
  duration = str(eval(arrivalTime)-eval(departureTime))
  return (departureAirport,arrivalAirport,departureTime,arrivalTime,flightCode,ticketPrice,duration)
  pass


if __name__ == '__main__':
  print launch_API('HEL','LHR','20151201000000','20151202000000')
  pass