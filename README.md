# Repositorio para Final de la Materia Ciencias de la Computación 2.
### Se buscaba resolver el problema de complejidad, el escenario a resolver es la asignacion de votantes a sus centros de votacion teniendo como fin que sea la forma mas rápida posible el proceso del recorrido a la hora de ir a votar
### Para ello, se buscaron diferentes soluciones las cuales se presentaron en la exposicion final de la cursada, como quedó trabajo para desarrollar se decidió presentar la aplicación de una solución pensada por el grupo.
### Optando por una opción semi-automática, buscamos que el usuario ingrese sus datos y en base a cálculos referidos a las coordenadas mas cercanas con los diferentes puntos de votacion que estan almacenados geográficamente, seleccionar el mas cercano.
### Se estableció un límite en la presentación de la aplicación, solamente se resolvió la lógica de la asignación de punto de votación en base a la información proporcionada por el usuario.
### Se muestra el punto mas cercano, su distancia y el tiempo de recorrido.


- Se utilizó la herramienta Nominatim ( https://nominatim.org/ ) de OpenStreetMap para hacer calculo de coordenadas. 
- Utilizamos la fórmula de Haversine para calcular distancias de las coordenadas.
- Se utilizó la API de  Openrouteservice ( https://openrouteservice.org/ ) para el trazado de rutas. 


Imagenes de la interfaz. 
- Menu principal.

![image](https://github.com/SantiPerez17/FinalCiencias2/assets/55918957/6ef8a510-f9cd-4c64-b266-e8c3daaf869b)

- Consulta de datos y muestra de resultados.
![image](https://github.com/SantiPerez17/FinalCiencias2/assets/55918957/1c7ab167-744e-4ed3-98a3-441a2c24875b)




Se aclara que esta solución se limitó al caso de la localidad de Pergamino y la localidad de Junín.

# Cambios a futuro.
- Carga automatizada de puntos de votación en base a una localidad/ciudad/región.
- Mejora de interfaz.
- Almacenamiento de datos en una base de datos.
- Utilizar una herramienta más eficiente como el Servicio Distance Matrix.
- Automatizar para que la búsqueda se realice en una cuadra/zona y en base a los habitantes de dicha cuadra/zona se los asigne al punto mas cercano.

