'''
Implementación de un sistema de gestión de datos en un invernadero a través del uso de un sensor de temperatura.
'''
import time, random

# Primero implementamos el patrón observador:
class Subscriptor:
    def actualizar(self, temperatura):
        #raise NotImplementedError("Es necesario implementar el método actualizar")
        print(f"Nueva temperatura: {temperatura}")

class SensorTemperatura:
    def __init__(self):
        self.suscriptores = [] # lista de subscriptores

    def alta(self, subscriptor):
        self.suscriptores.append(subscriptor) # para dar de alta un subscriptor lo añadimos a la lista

    def baja(self, subscriptor):
        try:
            self.suscriptores.remove(subscriptor) # para dar de baja un subscriptor lo sacamos de la lista
        except ValueError:
            return None

    def notificar_subscriptores(self, temperatura):
        for subscriptor in self.suscriptores:
            try:
                subscriptor.actualizar(temperatura) # para cada subscriptor actualizmos la temperatura
            except Exception as e:
                return f'Error: {e}'


# Ahora implementamos el patrón singleton:
class SistemaIoT:
    _unica_instancia = None # es un atributo no accesible fuera de la clase

    def __init__(self):
        if SistemaIoT._unica_instancia is not None:
            raise Exception("Debe ser un Singleton: única instancia")
        self.temperaturas = []

    @classmethod
    def obtener_instancia(cls): # nos aseguramos de que exista una instancia
        if not cls._unica_instancia:
            cls._unica_instancia = cls()
        return cls._unica_instancia
    
    def añadir_temperatura(self, timestamp, t):
        self.temperaturas.append((timestamp, t))  # al añadirse una nueva temperatura se añade a la lista temperaturas

    def obtener_temperatura(self):
        return self.temperaturas

    def contar_subscriptores(self):
        if len(SensorTemperatura().suscriptores) == 0: # si no hay susbscriptores salta un error
            raise ValueError("Debe haber susbcriptores")
        else:
            return len(SensorTemperatura().suscriptores) # para contar los subscriptores contamos el número de datos en la lista subscriptores
        


if __name__ == "__main__":

    # Inicializamos las clases:
    try:
        subscriptor_1 = Subscriptor()
        sensor = SensorTemperatura()
        sistema_iot = SistemaIoT.obtener_instancia()

        sensor.alta(subscriptor_1) # damos de alta al nuevo susbcriptor

        while True: # mientras se cumpla:
            tiempo = time.time() # tomamos la hora

            temperatura_randomiser = random.uniform(10, 40) # con uniform cogemos una temperatura cualquiera entre esos dos límites
            sistema_iot.añadir_temperatura(tiempo, temperatura_randomiser) # añadimos el timestamp y la temperatura
            sensor.notificar_subscriptores(temperatura_randomiser) # notificamos a los subscriptores con el nuevo dato

            if 10 < temperatura_randomiser > 38:
                sensor.baja(subscriptor_1)

            time.sleep(5) # el proceso se hará cada 5 segundos

    except KeyboardInterrupt:
        print(f"Se ha interrumpido el bucle") # de esta manera se puede interrumpir el while al hacer Ctrl + C