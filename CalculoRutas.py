import sys
from time import time
import requests
import openrouteservice
import json
import os
from haversine import haversine
import webbrowser

os.system('cls')
#Pedido de datos al usuario
ciudad = input('\n  --  Ingrese Ciudad: ')
nombrecalle = input('\n  --  Ingrese Nombre de Calle: ')
numerocalle = input('\n  --  Ingrese Número de Calle: ')

# Inicializamos el cliente de ORS
client = openrouteservice.Client(
    key='5b3ce3597851110001cf6248387fae09018f4103abd7a121e451863f')
#Asignamos a url la url del API nominatim para saber los datos
url = "https://nominatim.openstreetmap.org/?addressdetails=1&q=" + \
    numerocalle+","+nombrecalle+","+ciudad+"&format=json&limit=1"
#asignamos a res el pedido de tipo get que le hacemos a la API con la url anterior
res = requests.get(url)
#Si no encuentra la calle cierra el programa y muestra que no se encontró el domicilio
if res.json() == []:
    print('')
    print('No se encontró el domicilio')
    sys.exit('')
else:
    resultado = res.json()[0] #Si lo encuentra manda la respuesta que se recibió de la peticion en formato JSON

#Inicializamos un diccionario, que tendrá como clave 'calculo_temporal' y valor de la clave una lista vacía 
distancias_minimas = {}
distancias_minimas['calculo_temporal'] = []

#Función que devuelve la latitud y longitud de un archivo JSON 
def coordenadas_Domicilio(resultado):
    la = float(resultado['lat'])
    lo = float(resultado['lon'])
    return (la, lo)

#Funcion json_temporal, recibe como parámetro las mesas y un conjunto con latitud y longitud.
def json_temporal(mesas, latlon):
    for i in mesas['features']: #Recorremos las mesas
        a = i['geometry']['coordinates'] #Asignamos a la variable 'a' el valor de las coordenadas
        distancias_minimas['calculo_temporal'].append({ #agregamo a la lista vacía del diccionario los valores en formato JSON a continuación
            'origen': nombrecalle + ' ' + str(numerocalle),
            'latitudorigen': float(resultado['lat']),
            'longitudorigen': float(resultado['lon']),
            'destino': i['properties']["Name"],
            'latituddestino': float(a[1]),
            'longituddestino': float(a[0]),
            'distancia': haversine(latlon, (float(a[1]), float(a[0]))) #Utilizamos la fórmula de Haversine para calcular distancias en la tierra
        })
    distancias_minimas['calculo_temporal'].sort(
        key=lambda x: x["distancia"])  # ordenar por distancia
    with open('data_temporal.json', 'w') as file: #escribimos el diccionario en el archivo 'data_temporal.json'
        json.dump(distancias_minimas, file, indent=4)

#Funcion que ordena por distancia
def sort_by_key(list):
    return list['distancia']

#Funcion para armar el archivo data_temporal en base a la ciudad elegida.
def armar_json_distancias(resultado):
    if '2700' in resultado['display_name']: #Caso Pergamino
        with open('Pergamino_Mesas.geojson', encoding='utf-8-sig') as file:
            mesas = json.load(file)
            json_temporal(mesas, coordenadas_Domicilio(resultado))
    elif '6000' in resultado['display_name']: #Caso Junin
        with open('Junin_Mesas.geojson', encoding='utf-8-sig') as file:
            mesas = json.load(file)
            json_temporal(mesas, coordenadas_Domicilio(resultado))
    else: #Caso ciudad no encontrada
        print('')
        print('No se encontró el domicilio')
        sys.exit('')

#Se invoca la funcion que crea el JSON temporal que tiene los datos de origen y destino
#y se ordena en base a la distancia de menor a mayor
armar_json_distancias(resultado)

#Funcion que calcula la distancia y el tiempo del recorrido en base a un numero 'n'
def calc_Tiempo_Distancia(n):
    with open('data_temporal.json') as file: #Leemos el archivo 'data_temporal.json'
        calculo_distancias = json.load(file)
    for i in range(0, n): #En base al n recibido es la cantidad de rutas que va a calcular
        datos = calculo_distancias['calculo_temporal'][i] #extrae los datos de cada elemento del archivo JSON
        coords = ((str(datos['longitudorigen']), str(datos['latitudorigen'])),
                  (str(datos['longituddestino']), str(datos['latituddestino']))) #asignamos a coords las coordenadas origen y destino

        #En base al perfil(en auto o caminando) nos fijamos el cliente inicializado anteriormente los asignamos
        #a su variable correspondiente donde nos fijaremos donde está el tiempo y distancia.

        distydurauto = client.directions(
            coords, profile='driving-car')['routes'][0]['summary']
        distydurcaminando = client.directions(
            coords, profile='foot-walking')['routes'][0]['summary']

        #Asignación de variables
        origen = datos['origen']
        destino = datos['destino']
        duracionauto = distydurauto['duration']
        distanciaauto = distydurauto['distance']
        duracioncaminando = distydurcaminando['duration']
        distanciacaminando = distydurcaminando['distance']

        #Muestra en consola de resultados
        print(
            f'\nOrigen {origen.capitalize()} --> Destino {destino.capitalize()} \nAuto : [tiempo {round(duracionauto/60,3)} y distancia {round(distanciaauto/1000,3)}] \nCaminando : [tiempo {round(duracioncaminando/60,3)} y distancia {round(distanciacaminando/1000,3)}] ')

        #Se abre un navegador para comparar los resultados con el servicio de GoogleMaps
        webbrowser.open('https://www.google.com.ar/maps/dir/' +
                        str(datos['origen'])+' '+ciudad+'/'+str(datos['destino'])+' '+ciudad)
        with open('data_temporal.json', 'r+') as f:
            f.truncate()

#Si data_temporal.json no está vacío iniciamos el programa invocando a la funcion de calcular tiempo y distancia-
#Se calcula tambien cuanto tarda en hacerlo
if os.stat('data_temporal.json').st_size != 0:
    start_time = time()
    calc_Tiempo_Distancia(1)
    elapsed_time = time() - start_time
    print("Elapsed time: %0.10f seconds." % elapsed_time)
