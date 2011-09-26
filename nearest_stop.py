from pymongo import Connection, json_util
import simplejson as json

class Stops(object):

  def get_nearest_stops(self, lat, lon, limit):
    connection = Connection()
    db = connection.countdown
    stops = db.stops
    
    nearestStops = list( stops.find({ "loc": { "$near" : [ float(lat), float(lon) ] } }).limit(int(limit)) ) 
    
    json_data = json.dumps(nearestStops, default=json_util.default)
   
    return json_data

