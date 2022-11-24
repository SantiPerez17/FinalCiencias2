import openrouteservice
from openrouteservice import convert
import requests
import json



coords = (('-60.5982226','-33.886144'), ('-60.5701553','-33.9053091'))

client = openrouteservice.Client(key='5b3ce3597851110001cf6248387fae09018f4103abd7a121e451863f') # Specify your personal API key
routes = client.directions(coords,profile='cycling-regular')

a = requests.get('https://api.openrouteservice.org/v2/directions/cycling-regular?api_key=5b3ce3597851110001cf6248387fae09018f4103abd7a121e451863f&start=-60.5982226,-33.886144&end=-60.5701553,-33.9053091')
print(a.json())

l=routes['routes'][0]['summary']
print(l['distance']/1000, ' km.', l['duration']/60,' min.')
