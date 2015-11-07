from worker import findThem 

def search(homeCity, citys, startTime, endTime):
    """
    Parameters:
    -----------
    homeCity: "Helsinki"
    citys: ["Paris", "Rome"]
    startTime:  "2015-11-01"
    endTime: "2015-11-17"

    Returns: JSON
    --------
    {
      "options": 
      [ 
        { "totalPrice": "560.80", 
          "trips": [ {"FLN":"AY060", "startCity": "Helsinki", "endCity": "Rome", "startTime": "2015-11-01 08:30", "endTime": "2015-11-01 10:30", "price": 200.90},
                     {"FLN":"AY454", "startCity": "Rome", "endCity": "Paris", "startTime": "2015-11-04 14:30", "endTime": "2015-11-04 16:00", "price": 189.10},
                     {"FLN","AY981", "startCity": "Paris", "endCity": "Helsinki", "startTime": "2015-11-07 20:30", "endTime": "2015-11-07 22:00", "price": 170.80}]
        },

        { "totalPrice": "610.80", 
          "trips": [ {"FLN":"AY234", "startCity": "Helsinki", "endCity": "Paris", "startTime": "2015-11-01 08:30", "endTime": "2015-11-01 10:30", "price": 250.90},
                     {"FLN":"AY312", "startCity": "Paris", "endCity": "Rome", "startTime": "2015-11-04 14:30", "endTime": "2015-11-04 16:00", "price": 189.10},
                     {"FLN":"AY632", "startCity": "Rome", "endCity": "Helsinki", "startTime": "2015-11-07 20:30", "endTime": "2015-11-07 22:00", "price": 170.80}]
        }        
      ]
    }
        
    """
    return findThem(homeCity, citys, startTime, endTime)

if __name__ == "__main__":
    print search("Helsinki", ["Munich", "Milan", "Berlin"], "2015-12-01","2015-12-15")
