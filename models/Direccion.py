class Direccion:
    def __init__(self,nombre,numero,calle,latitud,longitud,ciudad):
        self.nombre = nombre
        self.numero = numero
        self.calle= calle
        self.latitud = latitud
        self.longitud = longitud
        self.ciudad = ciudad
    
    def __str__(self):
        return f'[nombre: {self.nombre} | numero: {self.numero} | calle: {self.calle} | latitud: {self.latitud} | longitud: {self.longitud} | ciudad: {self.ciudad}]' 

    def serialize(self):
        return {
            "nombre": self.nombre,
            "latitud": self.latitud,
            "longitud": self.longitud,
            "ciudad": self.ciudad
        }
