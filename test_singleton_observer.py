import pytest, time
from singleton_observer import Subscriptor, SensorTemperatura, SistemaIoT

def test_notificar_subscriptores():
    subscriptor_1 = Subscriptor()
    subscriptor_2 = Subscriptor()
    sensor = SensorTemperatura()

    sensor.alta(subscriptor_1) # primero damos de alta al subscriptor
    sensor.alta(subscriptor_2)

    temperatura = 31
    sensor.notificar_subscriptores(temperatura)  # notificamos de la temperatura al subcriptor
    assert subscriptor_1.actualizar(temperatura) == 31 # vemos si se ha actualizado correctamente
    assert subscriptor_2.actualizar(temperatura) == 31


def test_alta_baja():
    # inicializamos susbcriptor y sensor:
    subscriptor_1 = Subscriptor()
    subscriptor_2 = Subscriptor()
    sensor = SensorTemperatura()
    
    sensor.alta(subscriptor_1) # damos de alta a los subscriptores
    sensor.alta(subscriptor_2)
    assert len(sensor.suscriptores) == 2 # comprobamos que sean 2

    sensor.baja(subscriptor_1) # damos de baja
    assert len(sensor.suscriptores) == 1 # comprobamos que sea 1


def test_añadir_temperatura():
    sistema = SistemaIoT.obtener_instancia()
    tiempo = time.time() # tomamos la hora

    temperatura = 14
    sistema.añadir_temperatura(tiempo, temperatura) # añadimos timestamp y t
    assert (tiempo, temperatura) in sistema.obtener_temperatura() # comprobamos que se pueda obtener la temperatura añadida

if __name__ == "__main__":
    pytest.main([__file__])  # ¡Comprobamos que todos los tests han dado el resultado que se esperaba! :)