from singleton_observer import SistemaIoT, SensorTemperatura, Subscriptor
from chain_strategy import ManejadorEstadisticos, ManejadorIncremento, ManejadorUmbral
from chain_strategy import ComputarEstadisticoCuantiles, ComputarEstadisticoMaxMin, ComputarEstadisticoMediaDesv
from kafka import KafkaConsumer, KafkaProducer, KafkaError
import time, random
import json

# Inicializamos el productor y el consumidor, estableciendo conexión:

class Producer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers='localhost:9092', # este localhost nos indica que kafka funciona en la máquina local del consumer
            value_deserializer=lambda x: json.loads(x.encode('utf-8'))) 

    # eneviamos la temepratura a Kafka:
    def simular_envio_temperaturas(self, sensor, sistema_iot):
        # al igual que en el código de prueba, tomamos la hora y una temperatura cualquiera entre 10 y 40 grados:
        tiempo = time.time()
        temperatura = random.uniform(10, 40)

        sistema_iot.añadir_temperatura(tiempo, temperatura)
        sensor.notificar_subscriptores(temperatura)

        datos_temperatura = {'timestamp': tiempo, 't': temperatura} # imprimos los datos acorde al entregable
        mandar_datos = self.producer.send('temperatura-sistemaiot', datos_temperatura) # mandamos esos datos al consumidor

        try:
            mandar_datos.get(timeout=15)
            print(f"Datos: {datos_temperatura}")
        except KafkaError as e:
            print(f"Error: {e}")

class Consumer:
    def __init__(self):
        self.consumer = KafkaConsumer('temperatura-sistemaiot', 
                        bootstrap_servers='localhost:9092', # 9092 es el puerto defecto de Kafka
                        value_deserializer=lambda x: json.loads(x.decode('utf-8'))) 

    # kafka recibe los datos:
    def recibir_envio_temperaturas(self, sensor, sistema_iot):
        for mensaje in self.consumer: # recorremos cada mensaje
            valor = mensaje.value # guardamos el dato de temperatura con su tiempo
            sistema_iot.añadir_temperatura(valor['timestamp'], valor['t']) # lo añadimos al sistema
            sensor.notificar_subscriptores(valor['t']) # notificamos a los subscriptores con el nuevo valor de la temperatura
            print(f"Datos: {valor}")

            # ahora añadimos los manejadores:
            # primer los instanciamos
            manejador_umbral = ManejadorUmbral()
            manejador_incremento = ManejadorIncremento()
            manejador_estadisticos_mediadesv = ManejadorEstadisticos(ComputarEstadisticoMediaDesv())
            manejador_estadisticos_cuantiles = ManejadorEstadisticos(ComputarEstadisticoCuantiles())
            manejador_estadisticos_maxmin = ManejadorEstadisticos(ComputarEstadisticoMaxMin())

            # finalmente añadimos la temeperatura e imprimimos los resultados:
            print(f"Umbral: {manejador_umbral.manejar_temperatura(valor['t'])}")

            manejador_incremento.manejar_temperatura(valor['t'])
            print(f"Media , desviación: {manejador_estadisticos_mediadesv.manejar_temperatura(valor['t'])}")
            print(f"Cuantiles: {manejador_estadisticos_cuantiles.manejar_temperatura(valor['t'])}")
            print(f"Max y Min: {manejador_estadisticos_maxmin.manejar_temperatura(valor['t'])}")


# Codigo de prueba:
if __name__ == "__main__":

    while True:
        try: 
            # Inicializamos las diferentes clases:
            sistema_iot = SistemaIoT.obtener_instancia()
            sensor = SensorTemperatura()
            subscriptor = Subscriptor()
            consumidor = Consumer()
            productor = Producer()

            sensor.alta(subscriptor)

            productor.simular_envio_temperaturas(sensor, sistema_iot)
            consumidor.recibir_envio_temperaturas(sensor, sistema_iot)
            time.sleep(5)

        except KeyboardInterrupt:
            print(f"Se ha interrumpido el bucle") # de esta manera se puede interrumpir el while al hacer Ctrl + C