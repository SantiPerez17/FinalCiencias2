from time import sleep, time
import requests
import openrouteservice
import json
import os
from haversine import haversine
import webbrowser

#Declaración de 3 variables utilizadas para que el usuario ingrese la información
ciudad = ""
nombrecalle = ""
numerocalle = ""

rutas = {}
rutas['rutas'] = []
rutas['lista'] = []
client = openrouteservice.Client(
    key='5b3ce3597851110001cf6248387fae09018f4103abd7a121e451863f')


def Inicializar(ciu, nom, num):
    os.system('cls')
    # Pedido de datos al usuario
    ciudad = ciu
    nombrecalle = nom
    numerocalle = num
    resultado = {}
    r = []

    # Asignamos a url la url del API nominatim para saber los datos
    url = "https://nominatim.openstreetmap.org/search?addressdetails=1&q=" + \
        numerocalle+","+nombrecalle+","+ciudad+"&format=json&limit=1"
    # asignamos a res el pedido de tipo get que le hacemos a la API con la url anterior
    res = requests.get(url)
    # Si no encuentra la calle cierra el programa y muestra que no se encontró el domicilio
    if res.json() == []:
        print('')
        print('No se encontró el domicilio')
        # sys.exit('')
        return ["No se encontró el domicilio"]
    else:
        # Si lo encuentra manda la respuesta que se recibió de la peticion en formato JSON
        resultado = res.json()[0]

    # Se invoca la funcion que crea el JSON temporal que tiene los datos de origen y destino
    # y se ordena en base a la distancia de menor a mayor
    armar_json_distancias(resultado, nombrecalle, numerocalle)

    # Si data_temporal.json no está vacío iniciamos el programa invocando a la funcion de calcular tiempo y distancia-
    # Se calcula tambien cuanto tarda en hacerlo
    if os.stat('data_temporal.json').st_size != 0:
        start_time = time()
        r = calc_Tiempo_Distancia(1, ciudad)
        elapsed_time = time() - start_time
        print("Tiempo: %0.10f segundos." % elapsed_time)
        r.append("Tiempo : %0.10f segundos." % elapsed_time)
        return r

# Función que devuelve la latitud y longitud de un archivo JSON
def coordenadas_Domicilio(resultado):
    la = float(resultado['lat'])
    lo = float(resultado['lon'])
    return (la, lo)

# Funcion json_temporal, recibe como parámetro las mesas y un conjunto con latitud y longitud.


def json_temporal(mesas, latlon, resultado, nombrecalle, numerocalle):
    # Inicializamos un diccionario, que tendrá como clave 'calculo_temporal' y valor de la clave una lista vacía
    distancias_minimas = {}
    distancias_minimas['calculo_temporal'] = []
    for i in mesas['features']:  # Recorremos las mesas
        # Asignamos a la variable 'a' el valor de las coordenadas
        a = i['geometry']['coordinates']
        distancias_minimas['calculo_temporal'].append({  # agregamo a la lista vacía del diccionario los valores en formato JSON a continuación
            'origen': nombrecalle + ' ' + str(numerocalle),
            'latitudorigen': float(resultado['lat']),
            'longitudorigen': float(resultado['lon']),
            'destino': i['properties']["Name"],
            'direccion_destino' : i['properties']["Direccion"],
            'latituddestino': float(a[1]),
            'longituddestino': float(a[0]),
            # Utilizamos la fórmula de Haversine para calcular distancias en la tierra
            'distancia': haversine(latlon, (float(a[1]), float(a[0])))
        })
    distancias_minimas['calculo_temporal'].sort(
        key=lambda x: x["distancia"])  # ordenar por distancia
    # escribimos el diccionario en el archivo 'data_temporal.json'
    with open('data_temporal.json', 'w') as file:
        json.dump(distancias_minimas, file, indent=4)


# Funcion para armar el archivo data_temporal en base a la ciudad elegida.
def armar_json_distancias(resultado,nombrecalle, numerocalle):
    if '2700' in resultado['display_name']:  # Caso Pergamino
        with open('Pergamino_Mesas.geojson', encoding='utf-8-sig') as file:
            mesas = json.load(file)
            json_temporal(mesas, coordenadas_Domicilio(resultado), resultado,nombrecalle, numerocalle)
    elif '6000' in resultado['display_name']:  # Caso Junin
        with open('Junin_Mesas.geojson', encoding='utf-8-sig') as file:
            mesas = json.load(file)
            json_temporal(mesas, coordenadas_Domicilio(resultado), resultado,nombrecalle, numerocalle)
    else:  # Caso ciudad no encontrada
        print('')
        print('No se encontró el domicilio')
        # sys.exit('')
        return ["No se encontró el resultado"]

def checkList(origen):
    with open('rutas.json') as file:  # Leemos el archivo 'data_temporal.json'
        rutas = json.load(file)
    if origen in rutas['lista']:
        return True
    else:
        return False

def normalizarDistancia(distancia):
    if round(distancia/1000,3) >= 1:
        return str(round(distancia/1000,1)) + " km"
    else:
        return str(round(distancia,None)) + " metros"

# Funcion que calcula la distancia y el tiempo del recorrido en base a un numero 'n'
def calc_Tiempo_Distancia(n,ciudad):
    with open('data_temporal.json') as file:  # Leemos el archivo 'data_temporal.json'
        calculo_distancias = json.load(file)
    for i in range(0, n):  # En base al n recibido es la cantidad de rutas que va a calcular
        #calculo_distancias['calculo_temporal'][i]['origen'] = nomc + " " + numc
        # extrae los datos de cada elemento del archivo JSON
        datos = calculo_distancias['calculo_temporal'][i]
        if not checkList(datos['origen']):
            coords = ((str(datos['longitudorigen']), str(datos['latitudorigen'])),
                  (str(datos['longituddestino']), str(datos['latituddestino'])))  # asignamos a coords las coordenadas origen y destino

            # En base al perfil(en auto o caminando) nos fijamos el cliente inicializado anteriormente los asignamos
            # a su variable correspondiente donde nos fijaremos donde está el tiempo y distancia.

            distydurauto = client.directions(
                coords, profile='driving-car')['routes'][0]['summary']
            distydurcaminando = client.directions(
                coords, profile='foot-walking')['routes'][0]['summary']
            duracionauto = distydurauto['duration']
            distanciaauto = distydurauto['distance']
            duracioncaminando = distydurcaminando['duration']
            distanciacaminando = distydurcaminando['distance']
        else:
            with open('rutas.json') as file:  # Leemos el archivo 'data_temporal.json'
                rut = json.load(file)
            index = rut['lista'].index(datos['origen'])
            elemento = rut['rutas'][index]
            duracionauto = elemento['duracionAuto']
            distanciaauto = elemento['distanciaAuto']
            duracioncaminando = elemento['duracioncaminando']
            distanciacaminando = elemento['distanciacaminando']
        
        origen = datos['origen']
        destino = datos['destino']
        dir_destino = datos['direccion_destino']
        ciu=ciudad


        with open('rutas.json') as file:  # Leemos el archivo 'data_temporal.json'
                rutaa = json.load(file)
        if origen not in rutaa['lista']:
            nueva={
                "origen" : origen,
                "destino" : destino,
                "direccion_a_ir" : dir_destino,
                "duracionAuto": duracionauto,
                "distanciaAuto": distanciaauto,
                "duracioncaminando" : duracioncaminando,
                "distanciacaminando" : distanciacaminando,
                "ciudad": ciu,
            }
            rutaa['rutas'].append(nueva)
            rutaa['lista'].append(origen)
            with open('rutas.json', 'w') as file:
                json.dump(rutaa, file, indent=4)

        # Muestra en consola de resultados
        print(
            f'\nOrigen: {origen.capitalize()} --> Destino: {destino.capitalize()} \nDireccion : {dir_destino} \nAuto : [tiempo {round(duracionauto/60,None)} minutos y distancia {normalizarDistancia(distanciaauto)} ] \nCaminando : [tiempo {round(duracioncaminando/60,None)} minutos y distancia {normalizarDistancia(distanciacaminando)}] ')

        
        with open('data_temporal.json', 'r+') as f:
            f.truncate()

        #return f"\nOrigen: {origen.capitalize()} --> Destino: {destino.capitalize()} \nDireccion : {dir_destino} \nAuto : [tiempo {round(duracionauto/60,None)} minutos y distancia {normalizarDistancia(distanciaauto)}] \nCaminando : [tiempo {round(duracioncaminando/60,None)} minutos y distancia {normalizarDistancia(distanciacaminando)}] "
        return [origen,
                destino,
                dir_destino,
                ciudad,
                str(round(duracionauto/60,None)) + ' minutos.',
                normalizarDistancia(distanciaauto),
                str(round(duracioncaminando/60,None)) + " minutos.", 
                normalizarDistancia(distanciacaminando)]

def abrir_maps(origen,destino, ciu):
    # Se abre un navegador para comparar los resultados con el servicio de GoogleMaps
    webbrowser.open('https://www.google.com.ar/maps/dir/' +
        str(origen)+' '+ciu+'/'+str(destino)+' '+ciu)