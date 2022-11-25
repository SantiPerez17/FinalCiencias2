import openrouteservice
from openrouteservice import convert
import requests
import json
import webbrowser
from OSMPythonTools.nominatim import Nominatim
import googlemaps
"""
coords = (('-60.5982226','-33.886144'), ('-60.5701553','-33.9053091'))

client = openrouteservice.Client(key='5b3ce3597851110001cf6248387fae09018f4103abd7a121e451863f') # Specify your personal API key
routes = client.directions(coords,profile='cycling-regular')

a = requests.get('https://api.openrouteservice.org/v2/directions/cycling-regular?api_key=5b3ce3597851110001cf6248387fae09018f4103abd7a121e451863f&start=-60.5982226,-33.886144&end=-60.5701553,-33.9053091')
print(a.json())

l=routes['routes'][0]['summary']
print(l['distance']/1000, ' km.', l['duration']/60,' min.')


import requests

body = {"coordinates":[[8.681495,49.41461],[8.686507,49.41943],[8.687872,49.420318]]}

headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    'Authorization': '5b3ce3597851110001cf6248387fae09018f4103abd7a121e451863f',
    'Content-Type': 'application/json; charset=utf-8'
}
call = requests.post('https://api.openrouteservice.org/v2/directions/driving-car/gpx', json=body, headers=headers)

print(call.status_code, call.reason)
webbrowser.open_new(call.text)
nominatim = Nominatim()
heidelberg = nominatim.query("1535 francia")
print(heidelberg.address())
"""