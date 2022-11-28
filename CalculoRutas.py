import sys
from time import time
import requests
import openrouteservice
import json
import os
from haversine import haversine
import webbrowser

os.system('cls')

ciudad = input('\n  --  Ingrese Ciudad: ')
nombrecalle = input('\n  --  Ingrese Nombre de Calle: ')
numerocalle = input('\n  --  Ingrese Número de Calle: ')

# Inicializamos el cliente de ORS
client = openrouteservice.Client(
    key='5b3ce3597851110001cf6248387fae09018f4103abd7a121e451863f')

url = "https://nominatim.openstreetmap.org/?addressdetails=1&q=" + \
    numerocalle+","+nombrecalle+","+ciudad+"&format=json&limit=1"

res = requests.get(url)

if res.json() == []:
    print('')
    print('No se encontró el domicilio')
    sys.exit('')
else:
    resultado = res.json()[0]


distancias_minimas = {}
distancias_minimas['calculo_temporal'] = []


def coordenadas_Domicilio(resultado):
    la = float(resultado['lat'])
    lo = float(resultado['lon'])
    return (la, lo)


def json_temporal(mesas, latlon):
    for i in mesas['features']:
        a = i['geometry']['coordinates']
        distancias_minimas['calculo_temporal'].append({
            'origen': nombrecalle + ' ' + str(numerocalle),
            'latitudorigen': float(resultado['lat']),
            'longitudorigen': float(resultado['lon']),
            'destino': i['properties']["Name"],
            'latituddestino': float(a[1]),
            'longituddestino': float(a[0]),
            'distancia': haversine(latlon, (float(a[1]), float(a[0])))
        })
    distancias_minimas['calculo_temporal'].sort(
        key=lambda x: x["distancia"])  # ordenar por distancia
    with open('data_temporal.json', 'w') as file:
        json.dump(distancias_minimas, file, indent=4)


def sort_by_key(list):
    return list['distancia']


def armar_json_distancias(resultado):
    if '2700' in resultado['display_name']:
        with open('Pergamino_Mesas.geojson', encoding='utf-8-sig') as file:
            mesas = json.load(file)
            json_temporal(mesas, coordenadas_Domicilio(resultado))
    elif '6000' in resultado['display_name']:
        with open('Junin_Mesas.geojson', encoding='utf-8-sig') as file:
            mesas = json.load(file)
            json_temporal(mesas, coordenadas_Domicilio(resultado))
    else:
        print('')
        print('No se encontró el domicilio')
        sys.exit('')


armar_json_distancias(resultado)


def calc_Tiempo_Distancia(n):
    with open('data_temporal.json') as file:
        calculo_distancias = json.load(file)
    for i in range(0, n):
        datos = calculo_distancias['calculo_temporal'][i]
        coords = ((str(datos['longitudorigen']), str(datos['latitudorigen'])),
                  (str(datos['longituddestino']), str(datos['latituddestino'])))

        distydurauto = client.directions(
            coords, profile='driving-car')['routes'][0]['summary']
        distydurcaminando = client.directions(
            coords, profile='foot-walking')['routes'][0]['summary']

        origen = datos['origen']
        destino = datos['destino']
        duracionauto = distydurauto['duration']
        distanciaauto = distydurauto['distance']
        duracioncaminando = distydurcaminando['duration']
        distanciacaminando = distydurcaminando['distance']

        print(
            f'\nOrigen {origen.capitalize()} --> Destino {destino.capitalize()} \nAuto : [tiempo {round(duracionauto/60,3)} y distancia {round(distanciaauto/1000,3)}] \nCaminando : [tiempo {round(duracioncaminando/60,3)} y distancia {round(distanciacaminando/1000,3)}] ')

        webbrowser.open('https://www.google.com.ar/maps/dir/' +
                        str(datos['origen'])+' '+ciudad+'/'+str(datos['destino'])+' '+ciudad)
        with open('data_temporal.json', 'r+') as f:
            f.truncate()


if os.stat('data_temporal.json').st_size != 0:
    start_time = time()
    calc_Tiempo_Distancia(1)
    elapsed_time = time() - start_time
    print("Elapsed time: %0.10f seconds." % elapsed_time)
