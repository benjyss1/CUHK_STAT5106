# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 22:49:45 2019

@author: KY
"""

def getGeojs(address, verbose=False):
    import urllib.request, urllib.parse, urllib.error
    import json
    import ssl
    
    serviceurl = 'https://nominatim.openstreetmap.org/'

    if len(address) < 1: 
        print('==== Failure To Retrieve ====')
        print('Address is None Value.')
        return {}        

    parms = {}
    parms['q'] = address
    parms['addressdetails'] = 1
    parms['country'] = 'Hong Kong'
    parms['format'] = 'json'
    parms['limit'] = '1'
    url = serviceurl + '?' + urllib.parse.urlencode(parms)

    data = []
    if verbose: print('Retrieving', url)
    uh = urllib.request.urlopen(url)
    if verbose: print('Status', uh.status)
    if uh.status==200:  data = uh.read().decode()
    if verbose: print('Retrieved', len(data), 'characters')

    try:
        js = json.loads(data)[0]
    except:
        js = None

    if not js:
        print('==== Failure To Retrieve ====')
        print(data)
        return {}

    return js

def getGeojs_route(address_from, address_to, verbose=False):
    import urllib.request, urllib.parse, urllib.error
    import json
    import ssl

    if len(address_from) < 1 or len(address_to) < 1: 
        print('==== Failure To Retrieve ====')
        print('Address is None Value.')
        return {}  

    #Get geo json on both addr
    address_from_js = getGeojs(address_from)
    address_to_js = getGeojs(address_to)

    serviceurl = "http://router.project-osrm.org/route/v1/driving/"
    #Use lon and lat in the request
    serviceurl += "{0},{1};{2},{3}".format(address_from_js["lon"], address_from_js["lat"], address_to_js["lon"], address_to_js["lat"]) 

    parms = {}
    parms['overview'] = "full"
    parms['steps'] = 'true'
    parms["geometries"] = 'geojson'
    url = serviceurl + '?' + urllib.parse.urlencode(parms)

    #Flag to indicate data retrieved
    retrieved = False
    data = []

    #loop until received response from server
    while not retrieved:
      try: 
        if verbose: print('Retrieving', url)
        uh = urllib.request.urlopen(url)
        if verbose: print('Status', uh.status)
        if uh.status==200:  
          data = uh.read().decode()
          #update the flag to avoid infinite loop
          retrieved = True
        if verbose: print('Retrieved', len(data), 'characters')
      except:
        #update resp to None and the flag to avoid infinite loop
        js = None
        retrieved = True

    try:
        js = json.loads(data)
    except:
        js = None

    if not js:
        print('==== Failure To Retrieve ====')
        print(data)
        return {}

    return js


def getTunnelFares():
  return {
    'Aberdeen Tunnel': 5,
    'Lion Rock Tunnel': 8,
    'Shing Mun Tunnels': 5,
    'Shing Mun Tunnels': 5,
    'Tseung Kwan O Tunnel': 3,
    'Tsing Sha Highway': 8,
    'Cross Harbour Tunnel': 20,
    'Eastern Harbour Crossing': 40,
    'Western Harbour Crossing': 85,
    'Tate\'s Cairn Tunnel': 20,
    'Tai Lam Tunnel': 52
    }
