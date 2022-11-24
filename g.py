import requests
import json
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib.request





session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


nombrecalle = input('ingrese nombre de calle:')
numerocalle = input('ingrese numero: ')


api_key = 'ge-fd7e320a2c0f49fc'
query = "https://api.geocode.earth/v1/search?" \
        "api_key="+api_key+"&"\
        "text="+str(numerocalle)+","+str(nombrecalle)+",BA,Argentina"

response = json.load(urllib.request.urlopen(query))
print("cc",response['features'][0]['geometry']['coordinates'])


datatemporal={}
datatemporal['asignacion_de_escuelas']=[]
with open('Pergamino_Mesas.geojson', encoding='utf-8-sig') as file:
    mesas = json.load(file)

print(mesas['features'][0]['geometry']['coordinates'])

#requestaauto=session.get("https://localhost:8080/ors/v2/directions/driving-car?&start="+lon+","+lat+"&end="+str(mesas['features'][0]['geometry']['coordinates'][1])+","+str(mesas['features'][0]['geometry']['coordinates'][0]))
#session.close()
#r=requestaauto['features'][0]['properties']['segments']
#print(r[0]['distance'],r[0]['duration'])
"""for p in data['mesas_pergamino']:
    headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
}
    requestaauto=requests.get("https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf6248387fae09018f4103abd7a121e451863f&start="+lon+","+lat+"&end="+p['longitud']+","+p['latitud'], headers=headers)
    requestabicicleta=requests.get("https://api.openrouteservice.org/v2/directions/cycling-regular?api_key=5b3ce3597851110001cf6248387fae09018f4103abd7a121e451863f&start="+lon+","+lat+"&end="+p['longitud']+","+p['latitud'], headers=headers)
    requestamoto=requests.get("https://api.openrouteservice.org/v2/directions/foot-walking?api_key=5b3ce3597851110001cf6248387fae09018f4103abd7a121e451863f&start="+lon+","+lat+"&end="+p['longitud']+","+p['latitud'], headers=headers)
    print(requestaauto['features']['summary'])

    #requestabicicleta=client.directions((latylon,(p['longitud'],p['latitud'])),profile='cycling-regular')
    requestaauto=client.directions((latylon,(p['longitud'],p['latitud'])),profile='driving-car')
    requestacaminando=client.directions((latylon,(p['longitud'],p['latitud'])),profile='foot-walking')
    datatemporal['asignacion_de_escuelas'].append({
        'origen': nombrecalle + ' ' + str(numerocalle),
        'destino': p['nombre'],
        'distytiempo_con_bicicleta':{
            'distancia': requestabicicleta['routes'][0]['summary']['distance']/1000,
            'duracion' : requestabicicleta['routes'][0]['summary']['duration']/60,
        },
        'distytiempo_con_auto':{
            'distancia': requestaauto['routes'][0]['summary']['distance']/1000,
            'duracion' : requestaauto['routes'][0]['summary']['duration']/60,

        },
        'distytiempo_con_caminando':{
            'distancia': requestacaminando['routes'][0]['summary']['distance']/1000,
            'duracion' : requestacaminando['routes'][0]['summary']['duration']/60,
        }
    })
    with open('data_temporal.json', 'w') as file:
        json.dump(datatemporal, file, indent=4)
    fin=time.time()

print(fin-inicio)

"""

