import requests
import json
import os
from haversine import haversine

ciudad = input('ingrese ciudad: ')
nombrecalle = input('ingrese nombre de calle:')
numerocalle = input('ingrese numero: ')


def sort_by_key(list):
    return list['distancia']


url = "https://nominatim.openstreetmap.org/?addressdetails=1&q=" + \
    numerocalle+","+nombrecalle+","+ciudad+"&format=json&limit=1"
resultado = requests.get(url)

def coordenadas_Domicilio(resultado):
    return (float(resultado.json()[0]['lat']), float(resultado.json()[0]['lon']))


distancias_minimas = {}
distancias_minimas['calculo_temporal'] = []


def armar_json_distancias(resultado):
    latlon = coordenadas_Domicilio(resultado)
    if 'Pergamino' in resultado.json()[0]['display_name']:
        with open('Pergamino_Mesas.geojson', encoding='utf-8-sig') as file:
            mesas = json.load(file)
    elif 'Junín' in resultado.json()[0]['display_name']:
        with open('Junin_Mesas.geojson', encoding='utf-8-sig') as file:
            mesas = json.load(file)
    else:
        return 'domicilio no encontrado.'
    for i in mesas['features']:
        a = i['geometry']['coordinates']
        distancias_minimas['calculo_temporal'].append({
            'origen': nombrecalle + ' ' + str(numerocalle),
            'latitudorigen': float(resultado.json()[0]['lat']),
            'longitudorigen': float(resultado.json()[0]['lon']),
            'destino': i['properties']["Name"],
            'latituddestino': float(a[1]),
            'longituddestino': float(a[0]),
            'distancia': haversine(latlon, (float(a[1]), float(a[0])))
        })
    distancias_minimas['calculo_temporal'].sort(
        key=lambda x: x["distancia"])  # ordenar por distancia
    with open('data_temporal.json', 'w') as file:
        json.dump(distancias_minimas, file, indent=4)


def calc_Tiempo_Distancia(n):
    with open('data_temporal.json') as file:
        calculo_distancias = json.load(file)
    for i in range(0, n):
        datos = calculo_distancias['calculo_temporal'][i]
        urlauto = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf6248387fae09018f4103abd7a121e451863f&start=" + \
            str(datos['longitudorigen'])+","+str(datos['latitudorigen'])+"&end=" + \
            str(datos['longituddestino'])+","+str(datos['latituddestino'])
        urlcaminando = "https://api.openrouteservice.org/v2/directions/foot-walking?api_key=5b3ce3597851110001cf6248387fae09018f4103abd7a121e451863f&start=" + \
            str(datos['longitudorigen'])+","+str(datos['latitudorigen'])+"&end=" + \
            str(datos['longituddestino'])+","+str(datos['latituddestino'])

        distydurauto = requests.get(urlauto).json(
        )['features'][0]['properties']['summary']
        distydurcaminando = requests.get(urlcaminando).json()[
            'features'][0]['properties']['summary']

        origen = datos['origen']
        destino = datos['destino']
        duracionauto = distydurauto['duration']
        distanciaauto = distydurauto['distance']
        duracioncaminando = distydurcaminando['duration']
        distanciacaminando = distydurcaminando['distance']
        # print(requests.get(urlcaminando).json()['features'][0]['properties']['summary'])

        print(
            f'\nOrigen {origen.capitalize()} --> Destino {destino.capitalize()} \nAuto : [tiempo {round(duracionauto/60,3)} y distancia {round(distanciaauto/1000,3)}] \nCaminando : [tiempo {round(duracioncaminando/60,3)} y distancia {round(distanciacaminando/1000,3)}] ')


armar_json_distancias(resultado)

if os.stat('data_temporal.json').st_size != 0:
    calc_Tiempo_Distancia(1)
