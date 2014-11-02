# -*- coding: utf-8 -*-
"""
Created on Sun Nov  2 09:21:47 2014

@author: fodra
"""

import urllib
import simplejson

googleGeocodeUrl = 'http://maps.googleapis.com/maps/api/geocode/json?'

def get_coordinates(query, from_sensor=False):
    query = query.encode('utf-8')
    params = {
        'address': query,
        'sensor': "true" if from_sensor else "false"
    }
    url = googleGeocodeUrl + urllib.urlencode(params)
    json_response = urllib.urlopen(url)
    response = simplejson.loads(json_response.read())
    if response['results']:
        location = response['results'][0]['geometry']['location']
        latitude, longitude = location['lat'], location['lng']
    else:
        latitude, longitude = None, None
    return latitude, longitude
    
if __name__ == "main":
    print get_coordinates("32 rue Jacques Louis Bernier, Colombes")
    