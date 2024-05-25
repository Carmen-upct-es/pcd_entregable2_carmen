'''
Implementación de un sistema de gestión de datos en un invernadero a través del uso de un sensor de temperatura.
'''
from singleton_observer import SistemaIoT, SensorTemperatura, Subscriptor
import time, random
from functools import reduce

# Implementamos el patrón Strategy:
class ComputarEstadistico:

    def calcular_estadistico(self, temperaturas):
        raise NotImplementedError("Es necesario implementar el método calcular_estadistico")


class ComputarEstadisticoMediaDesv(ComputarEstadistico): # esta clase hereda de ComputarEstadistico
    def calcular_estadistico(self, temperaturas):
        total_datos = len(temperaturas) # para saber el número total de temperaturas hacemos len a las temperaturas

        # la media es la suma de todas las temperaturas(x + y) partido del nº total de ellas:
        media = reduce(lambda x, y: x + y, temperaturas) / total_datos # gracias añ reduce obtenemos un dato final

        # La desviación es la varianza ** 1/2. Utilizamos la fórmula para calcular la varianza según las temperaturas siendo 0 el valor inicial:
        desviacion_tipica = (reduce(lambda x, y: x + (y - media) ** 2, temperaturas, 0) / total_datos) ** (1 / 2) 
        return media, desviacion_tipica

class ComputarEstadisticoCuantiles(ComputarEstadistico):
    def calcular_estadistico(self, temperaturas):
        temperaturas_orden_asc = sorted(temperaturas) # ordenamos acendentemente cada temperatura en temperaturas
        total_datos = len(temperaturas_orden_asc)
        cuantil_1 = temperaturas_orden_asc[int(total_datos * 0.25)] # nos aseguramos que sea un entero
        cuantil_3 = temperaturas_orden_asc[int(total_datos * 0.75)]
        return cuantil_1, cuantil_3

class ComputarEstadisticoMaxMin(ComputarEstadistico):
    def calcular_estadistico(self, temperaturas): # para ver el max y min es tan simple como utilizar las propias funciones incluídas en python
        return max(temperaturas), min(temperaturas) # calculamos el max y min de la lista temperaturas



# Finalmente implementamos Chain of Responsibility:
class ManejadorTemperatura:
    def manejar_temperatura(self, temperatura):
        raise NotImplementedError("Es necesario implementar el método manejar_temperatura")


class ManejadorEstadisticos(ManejadorTemperatura):
    
    def __init__(self, estrategia: ComputarEstadistico): # le debemos marcar que la estrategia será la de ComputarEstadístico
        self.estrategia = estrategia
    
    def manejar_temperatura(self, temperatura):
        sistema_iot = SistemaIoT.obtener_instancia() # inicializamos una instancia del sistema
        tiempo = time.time() # tomamos la hora
    # obtenemos una lista haciendo un map con el primer elemento de temperatura y filtrando las temeperaturas con el tiempo en los últimos 60s:
        temperaturas = list(map(lambda t: t[1], filter(lambda t: tiempo - t[0] <= 60, sistema_iot.temperaturas)))
        return self.estrategia.calcular_estadistico(temperaturas) # dejamos que el cálculo de los estadisticos lo haga strategy


class ManejadorUmbral(ManejadorTemperatura):

    def manejar_temperatura(self, temperatura):
        umbral = 21 # el umbral será de 21 grados, una temperatura media
        if umbral != int:
        # Si se supera la temperatura del umbral, saltará un aviso, de lo contrario se notificará una temperatura normal:
            return "¡Cuidado! ¡Temperatura por encima del umbral!" if temperatura > umbral else "Temperatura normal"
        return ValueError


class ManejadorIncremento(ManejadorTemperatura):

    def manejar_temperatura(self, temperatura):
        sistema_iot = SistemaIoT.obtener_instancia() # inicializamos una instancia del sistema
        tiempo = time.time() # obtenemos la hora actual

        if not len(temperatura) > 2:
            return "Debe haber al menos dos datos de temperatura para poder ver un incremento"
        # al igual que en ManejadorEstadisticos obtenemos una lista de cada temperatura en los últimos 30s:
        temperaturas = list(map(lambda t: t[1], filter(lambda t: tiempo - t[0] <= 30, sistema_iot.temperaturas)))

        if temperaturas and (max(temperaturas) - min(temperaturas)) > 10: # si vemos que la diferencia entre el max y el min es mayor que 10:
            print("¡Cuidado! La temperatura ha aumentado más de 10º en los últimos 30 segundos")



if __name__ == "__main__":
# Realizamos la misma prueba que en el fichero singleton-observer añadiendo los manejadores:
    try:
        subscriptor_1 = Subscriptor()
        sensor = SensorTemperatura()
        sistema_iot = SistemaIoT.obtener_instancia()

        # inicializamos dos nuevas clases:
        manejador_estadisticos_mediadesv = ManejadorEstadisticos(ComputarEstadisticoMediaDesv())
        manejador_estadisticos_maxmin = ManejadorEstadisticos(ComputarEstadisticoMaxMin())
        manejador_umbral = ManejadorUmbral()

        sensor.alta(subscriptor_1)

        while True:
            tiempo = time.time()
            temperatura_randomiser = random.uniform(10, 40)
            sistema_iot.añadir_temperatura(tiempo, temperatura_randomiser)
            sensor.notificar_subscriptores(temperatura_randomiser)

            # hacemos los estadísticos, añadiendo la lista de temperaturas del sistema:
            print(f"Media , desviación: {manejador_estadisticos_mediadesv.manejar_temperatura(sistema_iot.temperaturas)}")
            print(f"Cuantiles: {manejador_estadisticos_maxmin.manejar_temperatura(sistema_iot.temperaturas)}")
            print(f"Umbral: {manejador_umbral.manejar_temperatura(temperatura_randomiser)}")

            if 10 < temperatura_randomiser > 38:
                sensor.baja(subscriptor_1)
            
            time.sleep(5)
            print("-----------------------")

    except KeyboardInterrupt:
        print(f"Se ha interrumpido el bucle")