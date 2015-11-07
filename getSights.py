import urllib
import json

def getData():
    citys = open("home_citys.txt").read().split("\n")
    category = "4deefb944765f83613cdba6e"

    for city in citys:
        url = "https://api.foursquare.com/v2/venues/search?client_id=QZN5SN0P5Q0DFENZZCJHQ30UXQFUO11IFBTHHKUTW1I4PLUC&client_secret=1MOZSBPTWOLEQQBMD0ZT2G3YQKC2PJUHSPGOFOEAYQIO1XTD&near=%s&categoryId=%s&v=20140806&m=foursquare" % (city, category)
        response = urllib.urlopen(url).read()
        data = json.loads(response)
        with open("sights/%s.json" % city, "w") as outfile:
            json.dump(data, outfile)

def getSightsByCity(city):

    citydata = json.loads(open("sights/%s.json" % city).read())
    attractions = []
    for venue in citydata["response"]["venues"]:
        oneplace = {}
        oneplace["name"] = venue["name"]
        oneplace["popularity"] = venue["stats"]["checkinsCount"]
        oneplace["price"] = "0"
        oneplace["duration"] = "1"
        attractions.append(oneplace)
    return attractions

if __name__ == "__main__":
    citys = open("home_citys.txt").read().split("\n")
    for city in citys:
        print city, len(getSightsByCity("Paris"))

