import pytest, time
from chain_strategy import ComputarEstadisticoMediaDesv, ComputarEstadisticoCuantiles, ComputarEstadisticoMaxMin
from chain_strategy import ManejadorUmbral, ManejadorIncremento
from singleton_observer import SistemaIoT

# Para todos los test en ComputarEstadistico vamos a introducir una lista de temperaturas y comprobar que
# los resultados de las operaciones dan el resultado correcto:

def test_calcular_estadistico_media_desv():
    computar_estadistico = ComputarEstadisticoMediaDesv() # inicializamos

    temperaturas = [11, 23, 41, 28, 14] # introducimos 5 datos y calculamos
    media, desviacion_tipica = computar_estadistico.calcular_estadistico(temperaturas)
    # comprobamos que los resultados sean correctos:
    assert media == pytest.approx(23.4) # es importante utilizar approx ya que hemos usado una función lambda por lo que el cálculo puede no ser exacto al 100%
    assert 10 < desviacion_tipica < 12 # aunque también podemos utilizar intervalos

def test_calcular_estadistico_cuantiles():
    computar_estadistico = ComputarEstadisticoCuantiles()

    temperaturas = [11, 23, 41, 28, 14]
    cuantil_1, mediana, cuantil_3 = computar_estadistico.calcular_estadistico(temperaturas)
    assert cuantil_1 == 14
    assert mediana != 45 # la mediana no es 45
    assert cuantil_3 == 28

def test_calcular_estadistico_max_min():
    computar_estadistico = ComputarEstadisticoMaxMin()

    temperaturas = [11, 23, 41, 28, 14]
    maximo, minimo = computar_estadistico.calcular_estadistico(temperaturas)
    assert maximo == 41
    assert minimo == 11


# Tests en manejador:

def test_manejar_temperatura_umbral(): # este test debe salir FALLIDO ya que no se cumple el umbral especificado en la función
    manejador_umbral = ManejadorUmbral()

    temperatura = 34
    resultado = manejador_umbral.manejar_temperatura(temperatura)
    assert resultado == "Temperatura normal"

def test_manejar_temperatura_incremento():
    sistema_iot = SistemaIoT.obtener_instancia() # instanciamos las clases
    manejador = ManejadorIncremento()
    tiempo = time.time() # tomamos la hora

    sistema_iot.añadir_temperatura(tiempo, 35) # añadimos nueva temperatura
    resultado = manejador.manejar_temperatura([35]) # añadimos ese dato al manejador

    assert resultado == "Debe haber al menos dos datos de temperatura para poder ver un incremento" # sólo hay un dato por lo que no se puede ver un incremento

if __name__ == "__main__":
    pytest.main([__file__])  # ¡Comprobamos que todos los tests han dado el resultado que se esperaba! :)