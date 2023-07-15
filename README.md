# Repositorio para Final de la Materia Ciencias de la Computación 2

Este repositorio contiene la solución desarrollada para el problema de asignación de votantes a centros de votación de manera eficiente. El objetivo principal del proyecto es agilizar el proceso de recorrido de los votantes hacia sus respectivos centros de votación.

## Descripción del problema

El problema consiste en asignar a cada votante el punto de votación más cercano a su domicilio, minimizando el tiempo y la distancia de recorrido. Para abordar esta problemática, se implementó una solución semi-automatizada que permite al usuario ingresar sus datos y, mediante cálculos basados en las coordenadas geográficas, seleccionar el punto de votación más cercano.

## Tecnologías utilizadas

El proyecto se basa en las siguientes tecnologías y herramientas:

- Nominatim (https://nominatim.org/): Se utilizó esta herramienta de OpenStreetMap para obtener las coordenadas geográficas a partir de las direcciones proporcionadas por los usuarios.
- Fórmula de Haversine: Se empleó esta fórmula matemática para calcular las distancias entre las coordenadas geográficas.
- Openrouteservice (https://openrouteservice.org/): Se utilizó la API de Openrouteservice para trazar las rutas y obtener los tiempos estimados de recorrido.

## Funcionalidades implementadas

El proyecto se enfoca en la lógica de asignación de puntos de votación en base a la información proporcionada por el usuario. A continuación, se describen las funcionalidades implementadas:

- Interfaz de usuario: Se desarrolló una interfaz sencilla que permite al usuario ingresar los datos de su domicilio, como ciudad, calle y número.
- Cálculo de coordenadas: Se utilizó Nominatim para obtener las coordenadas geográficas del domicilio ingresado por el usuario.
- Cálculo de distancias: Se empleó la fórmula de Haversine para calcular las distancias entre las coordenadas del domicilio y los diferentes puntos de votación almacenados geográficamente.
- Selección del punto más cercano: Se selecciona el punto de votación con la menor distancia al domicilio del votante.
- Presentación de resultados: Se muestran al usuario el punto de votación más cercano, la distancia a dicho punto y el tiempo estimado de recorrido.

## Limitaciones y mejoras futuras

El proyecto se ha limitado a abordar el caso específico de las localidades de Pergamino y Junín. A continuación, se mencionan algunas mejoras y cambios a futuro:

- Carga automatizada de puntos de votación para otras localidades, ciudades o regiones.
- Mejora de la interfaz de usuario para una mejor experiencia visual.
- Almacenamiento de los datos en una base de datos para una gestión más eficiente.
- Explorar opciones más eficientes, como el uso del Servicio Distance Matrix, para el cálculo de distancias.
- Automatizar la búsqueda y asignación de votantes en base a cuadras o zonas, considerando la densidad de población en cada área.

## Imágenes de la interfaz

A continuación, se presentan algunas capturas de pantalla de la interfaz de la aplicación:

- Menú principal:

![Menú principal](https://github.com/SantiPerez17/FinalCiencias2/assets/55918957/6ef8a510-f9cd-4c64-b266-e8c3daaf869b)

- Consulta de datos y resultados:

![Consulta de datos y resultados](https://github.com/SantiPerez17/FinalCiencias2/assets/55918957/1c7ab167-744e-4ed3-98a3-441a2c24875b)

## Contribuciones y cambios aportados

El código ha sido mejorado y optimizado en base a la eficiencia y legibilidad. Se han realizado cambios para eliminar funciones innecesarias y mejorar la estructura del código en general.

Esperamos que esta solución sea de utilidad y que pueda seguir siendo mejorada en el futuro para abordar nuevos desafíos y escenarios.
