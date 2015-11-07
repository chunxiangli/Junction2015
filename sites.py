


__author__ = 'Hongyu Su'
__version__= '0.1'

def find_sites(trips):
  '''
  fill in trip information
  '''
  print "----------------------------------------------------------------"
  tripsLen = len(trips)
  for i in xrange(tripsLen-1):
    city      = trips[i]['endCity']
    startTime = trips[i]['endTime']
    endTime   = trips[i+1]['startTime']
    print i,city,startTime,endTime
    
  res = []
  print "----------------------------------------------------------------"
  return res