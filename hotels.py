import urllib, json, random
from getSights import getHotelsByCity
from datetime import timedelta, datetime, tzinfo, time
import re
import random

CURRENCY = 'EUR'
top_num = 1

def read_city_code():
        city_code_dict = {}
        for line in open('ISO_city_code.txt', 'r').readlines():
                cC = line.split(':')
                city_code_dict[cC[0]] = cC[1]
        return city_code_dict

city_code_dict = read_city_code()

def find_myhotels(trips):
        hotels = []
        trip = trips[0]
        #check_in_date, in_time = trip["endTime"].split()
        check_in_date, in_time = extract_date_and_time(trip, 'in')
        city = trip["endCityName"]
        
        for trip in trips[1:]:
                check_out_date, out_time = extract_date_and_time(trip, 'out')
                #hotel = find_cheapest_hotel(city, CURRENCY, 'en_GB', '27539733', check_in_date, check_out_date, 1, 1)
                hotel = find_hotel_by_city(city)

                hotel["type"] = "hotel"
                hotel['city'] = city
                #hotel["startTime"] = "%s %s"%(check_in_date, in_time)
                hotel["startTime"] = "%s 23:00:00"%(check_in_date)
                #hotel["endTime"] = "%s %s"%(check_out_date, out_time)
                hotel["endTime"] = "%s 08:00:00"%(check_out_date)
                hotels.append(hotel)
                check_in_date, in_time= extract_date_and_time(trip, 'in')
                city = trip["endCityName"]
        return hotels


def find_hotels(trips):
  hotels = find_myhotels(trips)
  newhotels = []
  for item in hotels:
    startTime = item['startTime']
    endTime = item['endTime']
    startTime = datetime(int(startTime.split(' ')[0].split('-')[0]),int(startTime.split(' ')[0].split('-')[1]),int(startTime.split(' ')[0].split('-')[2]),int(startTime.split(' ')[1].split(':')[0]),int(startTime.split(' ')[1].split(':')[1]))
    endTime = datetime(int(endTime.split(' ')[0].split('-')[0]),int(endTime.split(' ')[0].split('-')[1]),int(endTime.split(' ')[0].split('-')[2]),int(endTime.split(' ')[1].split(':')[0]),int(endTime.split(' ')[1].split(':')[1]))
    while startTime.day<endTime.day:
      item['startTime'] = re.sub('T',' ',startTime.isoformat())
      startTime += timedelta(days=1)
      item['endTime'] = re.sub('T',' ',datetime(startTime.year,startTime.month,startTime.day,random.randrange(6,8,1),0,0).isoformat())
      newhotels.append(item)
  return newhotels
  pass

#	{'city': 'Munich', 'name': u'ibis Muenchen City Arnulfpark', 'price': 250, 'popularity': 46, 'startTime': '2015-12-01 23:00:00', 'address': [u'Arnulfstrasse 55', u'80636 M\xfcnchen', u'Deutschland'], 'endTime': '2015-12-07 08:00:00', 'type': 'hotel'}



def extract_date_and_time(trip, t_type):
        if t_type == "in":
                check_date, check_time = trip["endTime"].split()
                check_time = correct_in_time(check_time)
        elif t_type == "out":
                check_date, check_time = trip["startTime"].split()
                check_time = correct_out_time(check_time)
        return check_date, check_time


def correct_in_time(t):
        hour, minute = split_time(t)
        if hour < 13:
                t = " 13:00"
        return t

def correct_out_time(t):
        hour, minute = split_time(t)
        if hour > 11:
                t = "11:00"
        return t

def split_time(t):

        return [int(v) for v in t.strip().split(':')[:-1]]

def find_hotel_by_city(city):
        hotels = getHotelsByCity(city)
        index = random.randrange(1, 10, 1)
        hotel = hotels[index]
        random_price = random.randrange(50,300,50)
        hotel["price"] = random_price
        return hotels[index]

#another option for choose cheapest hotel
def find_cheapest_hotel(city, currency, local, entityid, check_in_date, check_out_date, guests_num, room_number):

        city = city_code_dict[city]
        url = ['http://partners.api.skyscanner.net/apiservices/hotels/liveprices/v2']
        #'city UK/EUR/en-GB/27539733/2015-12-04/2015-12-10/2/1?apiKey=prtl6749387986743898559646983194'
        url.extend([city, currency, local, entityid, check_in_date, check_out_date, guests_num, '%d?apiKey=prtl6749387986743898559646983194'%room_number])

        response = urllib.urlopen('/'.join([str(u) for u in url]))

        res = json.loads(response.read())


        price_list = [] 
        hotel_ids = [] 
        for hp in res[u'hotels_prices']:
                price_list.append(hp[u'agent_prices'][0][u'price_total'])
                hotel_ids.append( hp[u'id'])

        top_two_index = sorted(range(len(price_list)), key=lambda k: price_list[k])[0:top_number]
        top_two_prices = [price_list[i] for i in top_two_index]
        top_two_hotel_ids = [hotel_ids[i] for i in top_two_index]

        hotels = {}

        for i in range(top_number):
                hotels[str(top_two_hotel_ids[i])] = {"type":"hotel", "City": city, "startTime": check_in_date, "endTime": check_out_date, 'price':top_two_prices[i]}

        #find top two hotel names
        for hp in res[u'hotels']:
                h_id = hp[u'hotel_id']
                if h_id in top_two_hotel_ids:
                        hotels[str(h_id)].update({'name': hp[u'name'].encode("utf-8")})
        hotel_list = []
        for i in range(top_number):
                hotel_list[i] = hotels[top_two_hotel_ids[i]]
        #return {"type":"hotel", "name": hotel_name, "City": city, "startTime": check_in_date, "endTime": check_out_date, "price": price}
        return hotel_list



