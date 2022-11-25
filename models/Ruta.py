class Ruta:
    def __init__(self,origen,destino,distancia,duracion):
        self.origen = origen,
        self.destino = destino,
        self.distancia = distancia,
        self.duracion = duracion
    
    def serialize(self):
        return {
            "origen": self.origen.nombre,
            "destino": self.destino.nombre,
            "distancia": self.distancia,
            "duracion": self.duracion
        }