import unittest
from buscaminas import ( crear_juego, en_rango,buscador_de_minas ,marcar_celda, obtener_estado_tablero_visible, descubrir_celda, verificar_victoria,
                         colocar_minas, calcular_numeros, todas_celdas_seguras_descubiertas, reiniciar_juego, guardar_estado, cargar_estado,
                         comas_en_lista, eliminar_saltos, sacar_repetidos, buscador ,BOMBA, BANDERA, VACIO, EstadoJuego)
from typing import Any

'''
Ayudamemoria: entre los métodos para testear están los siguientes:

    self.assertEqual(a, b) -> testea que a y b tengan el mismo valor
    self.assertTrue(x)     -> testea que x sea True
    self.assertFalse(x)    -> testea que x sea False
    self.assertIn(a, b)    -> testea que a esté en b (siendo b una lista o tupla)
'''     
#Tests originales
def cant_minas_en_tablero(tablero: list[list[int]]) -> int:
    """Chequea que el número de minas en el tablero sea igual al número de minas esperado"""
    contador_minas:int = 0
    for fila in tablero:
        for celda in fila:
            if celda == -1:
                contador_minas += 1
    return contador_minas

def son_solo_ceros_y_bombas (tablero: list[list[int]]) -> bool:
    for fila in tablero:
        for celda in fila:
            if celda not in [0, -1]:
                return False
    return True

def dimension_correcta(tablero: list[list[int]], filas: int, columnas: int) -> bool:
    """Chequea que el tablero tenga las dimensiones correctas"""
    if len(tablero) != filas:
        return False
    for fila in tablero:
        if len(fila) != columnas:
            return False
    return True
""" ------------------------------------ EJERCICIO 1--------------------------------------"""

class colocar_minasTest(unittest.TestCase):
    def test_ejemplo(self):
        filas:int = 2
        columnas:int = 2
        minas:int = 1
        
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        # Testeamos que el tablero tenga solo bombas o ceros
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(tablero), minas)

    
    def test_matriz_no_cuadrada (self): 
        filas:int = 2 
        columnas:int = 3 
        minas:int = 4 

        tablero: list[int[int]] = colocar_minas (filas, columnas, minas) 
        self.assertTrue (son_solo_ceros_y_bombas (tablero) )
        self.assertEqual (cant_minas_en_tablero (tablero), minas)

    def test_matriz_no_cuadrada_mas_filas (self): 
        filas:int = 4 
        columnas:int = 2 
        minas:int = 5 

        tablero: list[int[int]] = colocar_minas (filas,columnas,minas)
        self.assertTrue (son_solo_ceros_y_bombas (tablero))
        self.assertEqual (cant_minas_en_tablero (tablero),minas)


    def test_matriz_grande_muchas_bombas (self):
        filas:int = 10 
        columnas:int = 10 
        minas:int = 50 

        tablero: list[int[int]] = colocar_minas (filas,columnas,minas) 
        self.assertTrue (son_solo_ceros_y_bombas (tablero))
        self.assertEqual (cant_minas_en_tablero (tablero),minas)
    
    def test_matriz_sin_bombas(self):
        filas:int = 4
        columnas:int = 4
        minas:int = 0

        tablero: list[list[int]] = colocar_minas (filas,columnas,minas)
        self.assertTrue (son_solo_ceros_y_bombas (tablero))
        self.assertEqual (cant_minas_en_tablero (tablero),minas)

"----------------------------------- EJERCICIO 2-----------------------------------------"""

class en_rangoTest (unittest.TestCase): 
  # Testeamos la funcion auxiliar 
    def test_en_rango_False (self): 
        tablero: list[list[int]] = [[0,-1],[0,-1]] 
        f:int =1
        c:int =3 
        self.assertFalse (en_rango (tablero,f,c)) 

    def test_en_rango_True (self): 
        tablero:list[list[int]] = [[0,-1],[0,-1]] 
        f:int =1
        c:int =1 
        self.assertTrue (en_rango (tablero,f,c)) 

class buscador_de_minasTest (unittest.TestCase):
    def test_buscador_de_minas_ejemplo (self): 
        tablero: list[list[int]]= [[0,0,0],[-1,-1,0],[0,0,-1]]
        self.assertEqual (buscador_de_minas (tablero), [(1,0),(1,1),(2,2)])

class calcular_numerosTest(unittest.TestCase):
    def test_ejemplo(self):
        tablero:list[list[int]] = [[0,-1],[0, 0]]

        calcular_numeros(tablero)
        # Testeamos que el tablero tenga los números correctos
        self.assertEqual(tablero, [[1,-1],[1, 1]])

    def test_matriz_chica(self):
        tablero: list[list[int]] = [[0,0,-1],[0,0,-1],[0,0,0]]

        calcular_numeros(tablero)
        # Testeamos ue el tablero tenga los números correctos
        self.assertEqual(tablero,[[0,2,-1],[0,2,-1],[0,1,1]])
        self.assertFalse(son_solo_ceros_y_bombas(tablero))
    
    def test_matriz_grande(self):
        tablero: list[list[int]] = [[0,-1,0,0,0],[0,0,-1,0,0],[0,0,-1,0,-1],[0,0,0,0,0],[0,-1,-1,0,0]]

        calcular_numeros(tablero)
        self.assertEqual(tablero, [[1,-1,2,1,0],[1,3,-1,3,1],[0,2,-1,3,-1],[1,3,3,3,1],[1,-1,-1,1,0]])

    def test_solo_ceros(self):
        tablero: list[list[int]] = [[0,0],[0,0]]

        calcular_numeros(tablero)
        self.assertEqual(tablero,[[0,0],[0,0]])
    
    def test_un_solo_cero(self):
        tablero: list[list[int]]= [[-1,-1,0],[-1,0,0],[0,0,0]]

        calcular_numeros(tablero)
        self.assertEqual(tablero,[[-1,-1,1],[-1,3,1],[1,1,0]])
    
    def test_todas_bombas(self):
        tablero: list[list[int]]= [[-1,-1,-1],[-1,-1,-1],[-1,-1,-1]]

        calcular_numeros(tablero)
        self.assertEqual(tablero,[[-1,-1,-1],[-1,-1,-1],[-1,-1,-1]])

" -------------------------------------EJERCICIO 3 ---------------------------------------------------"        

class crear_juegoTest(unittest.TestCase):
    def test_ejemplo(self):
        filas:int = 2
        columnas:int = 2
        minas:int = 1
        estado: EstadoJuego = crear_juego(filas, columnas, minas)
        # Testeamos que el tablero tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero'], filas, columnas))
        # Testeamos que el tablero visible tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero_visible'], filas, columnas))
        # Testeamos que el tablero visible esté vacío
        for fila in estado['tablero_visible']:
            for celda in fila:
                self.assertEqual(celda, VACIO)
        # Testeamos que el resto es lo esperado
        self.assertEqual(estado['filas'], filas)
        self.assertEqual(estado['columnas'], columnas)
        self.assertEqual(estado['minas'], minas)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), minas)

    
    def test_tablero_grande(self):
        filas:int = 10
        columnas:int = 10
        minas:int = 20
        estado: EstadoJuego = crear_juego(filas, columnas, minas)
        # Testeamos que el tablero tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero'], filas, columnas))
        # Testeamos que el tablero visible tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero_visible'], filas, columnas))
        # Testeamos que el tablero visible esté vacío
        for fila in estado['tablero_visible']:
            for celda in fila:
                self.assertEqual(celda, VACIO)
        # Testeamos que el resto es lo esperado
        self.assertEqual(estado['filas'], filas)
        self.assertEqual(estado['columnas'], columnas)
        self.assertEqual(estado['minas'], minas)
        self.assertFalse(estado['juego_terminado'])
         # Testeamos que haya la cantidad de minas correctas en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), minas)

    def test_tablero_pequeño (self):
        filas:int = 2
        columnas:int = 2
        minas:int = 1
        estado: EstadoJuego = crear_juego(filas, columnas, minas)
        # Testeamos que el tablero tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero'], filas, columnas))
        # Testeamos que el tablero visible tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero_visible'], filas, columnas))
        # Testeamos que el tablero visible esté vacío
        for fila in estado['tablero_visible']:
            for celda in fila:
                self.assertEqual(celda, VACIO)
        # Testeamos que el resto es lo esperado
        self.assertEqual(estado['filas'], filas)
        self.assertEqual(estado['columnas'], columnas)
        self.assertEqual(estado['minas'], minas)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), minas)
    
    def test_tablero_solo_minas (self):
        filas:int = 3
        columnas:int = 3
        minas:int = 9
        estado: EstadoJuego = crear_juego(filas, columnas, minas)
        # Testeamos que el tablero tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero'], filas, columnas))
        # Testeamos que el tablero visible tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero_visible'], filas, columnas))
        # Testeamos que el tablero visible esté vacío
        for fila in estado['tablero_visible']:
            for celda in fila:
                self.assertEqual(celda, VACIO)
        # Testeamos que el resto es lo esperado
        self.assertEqual(estado['filas'], filas)
        self.assertEqual(estado['columnas'], columnas)
        self.assertEqual(estado['minas'], minas)
        self.assertFalse(estado['juego_terminado'])
         # Testeamos que haya la cantidad de minas correctas en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), minas)

    def test_tablero_una_minas (self):
        filas:int = 4
        columnas:int = 4
        minas:int = 1
        estado: EstadoJuego = crear_juego(filas, columnas, minas)
        # Testeamos que el tablero tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero'], filas, columnas))
        # Testeamos que el tablero visible tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero_visible'], filas, columnas))
        # Testeamos que el tablero visible esté vacío
        for fila in estado['tablero_visible']:
            for celda in fila:
                self.assertEqual(celda, VACIO)
        # Testeamos que el resto es lo esperado
        self.assertEqual(estado['filas'], filas)
        self.assertEqual(estado['columnas'], columnas)
        self.assertEqual(estado['minas'], minas)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una  mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), minas)

    def test_tablero_con_menos_filas(self):
        filas:int = 4
        columnas:int = 4
        minas:int = 1
        estado: EstadoJuego = crear_juego(2,columnas,minas)
        self.assertFalse(dimension_correcta(estado['tablero'], filas, columnas))
        # Testeamos que el tablero visible tenga las dimensiones correctas
        self.assertFalse(dimension_correcta(estado['tablero_visible'], filas, columnas))
        # Testeamos que el tablero visible esté vacío
        for fila in estado['tablero_visible']:
            for celda in fila:
                self.assertEqual(celda, VACIO)
        # Testeamos que el resto es lo esperado
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], columnas)
        self.assertEqual(estado['minas'], minas)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una  mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), minas)

    def test_tablero_con_menos_columnas(self):
        filas:int = 4
        columnas:int = 4
        minas:int = 1
        estado: EstadoJuego = crear_juego(filas,2,minas)
        self.assertFalse(dimension_correcta(estado['tablero'], filas, columnas))
        # Testeamos que el tablero visible tenga las dimensiones correctas
        self.assertFalse(dimension_correcta(estado['tablero_visible'], filas, columnas))
        # Testeamos que el tablero visible esté vacío
        for fila in estado['tablero_visible']:
            for celda in fila:
                self.assertEqual(celda, VACIO)
        # Testeamos que el resto es lo esperado
        self.assertEqual(estado['filas'], filas)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], minas)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una  mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), minas)

"----------------------------------------- EJERCICIO 4 ------------------------------------"

class obtener_estado_tableroTest(unittest.TestCase):
    
    def test_ejemplo(self):
        estado: EstadoJuego = {'filas': 2,'columnas': 2,'minas': 1,'tablero': [
            [-1, 1],
            [ 1, 1]],
            'tablero_visible': [
                [VACIO, "1"],
                [VACIO, VACIO]],
                'juego_terminado': False}

        # Testeamos que el estado del tablero sea el esperado
        self.assertEqual(obtener_estado_tablero_visible(estado), [[VACIO, "1"],[VACIO, VACIO]])
        
        # Testeamos que nada se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [[-1, 1],[ 1, 1]])
        self.assertEqual(estado['tablero_visible'],[[VACIO, "1"],[VACIO, VACIO]])
        self.assertFalse(estado['juego_terminado'])

    def test_juego_terminado (self): 
            estado: EstadoJuego = {'filas': 2,'columnas': 2,'minas': 1,'tablero': [
                [-1, 1],
                [ 1, 1]],
                'tablero_visible': [
                [BANDERA, "1"],
                ['1', '1']],
                'juego_terminado': True}
            
        # Testeamos que el estado del tablero sea el esperado
            self.assertEqual(obtener_estado_tablero_visible(estado), [[BANDERA, "1"],['1', '1']])
        
        # Testeamos que nada se modificó
            self.assertEqual(estado['filas'], 2)
            self.assertEqual(estado['columnas'], 2)
            self.assertEqual(estado['minas'], 1)
            self.assertEqual(estado['tablero'], [[-1, 1],[ 1, 1]])
            self.assertEqual(estado['tablero_visible'], [[BANDERA, "1"],['1', '1']])
            self.assertTrue(estado['juego_terminado'])

    def test_juego_sin_finalizar (self): 
            estado: EstadoJuego = {'filas': 2,'columnas': 2,'minas': 1,'tablero': [
                [-1, 1],
                [ 1, 1]],
            'tablero_visible': [
                [VACIO, "1"],
                ['1', VACIO]],
            'juego_terminado': False}

        # Testeamos que el estado del tablero sea el esperado
            self.assertEqual(obtener_estado_tablero_visible(estado), [[VACIO, "1"],['1', VACIO]])
        
        # Testeamos que nada se modificó
            self.assertEqual(estado['filas'], 2)
            self.assertEqual(estado['columnas'], 2)
            self.assertEqual(estado['minas'], 1)
            self.assertEqual(estado['tablero'], [[-1, 1],[ 1, 1]])
            self.assertEqual(estado['tablero_visible'], [[VACIO, "1"],['1', VACIO]])
            self.assertFalse(estado['juego_terminado'])

    def test_no_modifica_el_original(self):
        estado: EstadoJuego = {'filas': 2,'columnas': 2,'minas': 1,'tablero': [
                [-1, 1],
                [ 1, 1]],
            'tablero_visible': [
                [VACIO, "1"],
                ['1', VACIO]],
            'juego_terminado': False}
        
        modificable: list[list[str]] = obtener_estado_tablero_visible(estado)

        #modifico la primera entrada
        modificable[1][1] = BANDERA

        #verifico que el tablero original siga igual
        self.assertEqual(obtener_estado_tablero_visible(estado), [[VACIO, "1"],['1', VACIO]])

        # Testeamos que nada se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [[-1, 1],[ 1, 1]])
        self.assertEqual(estado['tablero_visible'], [[VACIO, "1"],['1', VACIO]])
        self.assertFalse(estado['juego_terminado'])

"-----------------------------------EJERCICIO 5 ----------------------------------------- "        

class marcar_celdaTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {'filas': 2,'columnas': 2,'minas': 1,'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }

        marcar_celda(estado, 0, 0)

        # Testeamos que sólo la celda marcada sea visible
        self.assertEqual(estado['tablero_visible'], [[BANDERA, VACIO],[VACIO, VACIO]])
        
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [[-1, 1],[1, 1]])
        self.assertFalse(estado['juego_terminado'])

        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)

    def test_marcar_celda_poner_bandera (self):
        estado: EstadoJuego = {'filas': 3,'columnas': 3,'minas': 1,
            'tablero': [
                [-1, 1, 0],
                [1, 1, 0 ],
                [0, 0, 0]
            ],
            'tablero_visible': [
                [VACIO, VACIO,VACIO],
                [VACIO, VACIO,VACIO],
                [VACIO,VACIO,VACIO]],
            'juego_terminado': False}
        
        marcar_celda(estado, 0, 0)
        
        # Testeamos que sólo la celda marcada sea visible
        self.assertEqual(estado['tablero_visible'], [[BANDERA, VACIO,VACIO],[VACIO, VACIO,VACIO],[VACIO,VACIO,VACIO]])
        
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [[-1, 1, 0],[1, 1, 0],[0, 0, 0]])
        self.assertFalse(estado['juego_terminado'])

        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)

    def test_marcar_celda_sacar_bandera (self): 
        # Testea cuando sacamos una bandera
        estado: EstadoJuego = {'filas': 2,'columnas': 2,'minas': 2,'tablero': [
                [-1, 2],
                [2, -1]],
            'tablero_visible': [
                [BANDERA, VACIO],
                [VACIO, VACIO]],
            'juego_terminado': False}
        
        marcar_celda(estado, 0, 0)

        # Testeamos que la celca volvio a ser vacío
        self.assertEqual(estado['tablero_visible'], [[VACIO, VACIO],[VACIO, VACIO]])
        
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [[-1, 2],[2, -1]])
        self.assertFalse(estado['juego_terminado'])

        # Teamos que hatya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 2)

    def test_tablero_semicubierto (self):
        estado: EstadoJuego = {'filas': 3,'columnas': 3,'minas': 1,'tablero': [
                [-1, 1, 0],
                [1, 1, 0 ],
                [0, 0, 0]],
            'tablero_visible': [
                [VACIO, VACIO,'0'],
                [VACIO, VACIO,'0'],
                ['0','0','0']],
            'juego_terminado': False}
        
        marcar_celda(estado, 0,1)
        
        # Testeamos que sólo la celda marcada sea visible
        self.assertEqual(estado['tablero_visible'], [[VACIO, BANDERA,'0'],[VACIO, VACIO,'0'],['0','0','0']])
        
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [[-1, 1, 0],[1, 1, 0],[0, 0, 0]])
        self.assertFalse(estado['juego_terminado'])

        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
    
    def test_marcar_uno_mas_de_una_vez (self): 
        estado: EstadoJuego = {'filas': 3,'columnas': 3,'minas': 3,'tablero': [
                [-1, 1, 0],
                [2, 3, 1 ],
                [-1, 2, -1]],
            'tablero_visible': [
                [VACIO, VACIO,VACIO],
                [VACIO, VACIO,VACIO],
                [VACIO,VACIO,VACIO]],
            'juego_terminado': False}
        
        marcar_celda(estado, 0,0)
        
        # Testeamos que sólo la celda marcada sea visible
        self.assertEqual(estado['tablero_visible'], [[BANDERA, VACIO,VACIO],[VACIO, VACIO,VACIO],[VACIO,VACIO,VACIO]])
        
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 3)
        self.assertEqual(estado['tablero'], [[-1, 1, 0],[2, 3, 1],[-1, 2, -1]])
        self.assertFalse(estado['juego_terminado'])
        
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 3)

        marcar_celda(estado, 0,0)

        # Testeamos que la marcada vuelva a ser vacío
        self.assertEqual(estado['tablero_visible'], [[VACIO, VACIO,VACIO],[VACIO, VACIO,VACIO],[VACIO,VACIO,VACIO]])
        
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 3)
        self.assertEqual(estado['tablero'], [[-1, 1, 0],[2, 3, 1],[-1, 2, -1]])
        self.assertFalse(estado['juego_terminado'])

        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 3)

    def test_tablero_pequeño (self): 
        # Testea cuando sacamos una bandera
        estado: EstadoJuego = {'filas': 3,'columnas': 1,'minas': 1,'tablero': [
                [1],
                [-1],
                [1]],
            'tablero_visible': [
                [VACIO],
                [VACIO],
                [VACIO]],
            'juego_terminado': False}
        
        marcar_celda(estado, 0, 0)
        
        # Testeamos que sólo la celda marcada sea visible
        self.assertEqual(estado['tablero_visible'], [[BANDERA],[VACIO],[VACIO]])

        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 1)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [[1],[-1],[1]])
        self.assertFalse(estado['juego_terminado'])

        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)

    def test_partida_terminada (self):
        estado: EstadoJuego = {'filas': 3,'columnas': 3,'minas': 1,'tablero': [
                [-1, 1, 0],
                [1, 1, 0 ],
                [0, 0, 0]],
            'tablero_visible': [
                [BANDERA, '1','0'],
                ['1', '1','0'],
                ['0','0','0']],
            'juego_terminado': True}
        
        marcar_celda(estado, 0,0)
        
        # Testeamos que no se modifico ninguna celda, pues el juego esta terminado 
        self.assertEqual(estado['tablero_visible'], [[BANDERA, '1','0'],['1', '1','0'],['0','0','0']])
        
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [[-1, 1, 0],[1, 1, 0],[0, 0, 0]])
        self.assertTrue(estado['juego_terminado'])

        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)   

"--------------------------------------- EJERCICIO 6---------------------------------------"

class todas_celdas_seguras_descubiertasTest (unittest.TestCase): 
    def test_todas_celdas_seguras_cubiertas_true (self): 
        tablero = [[2,-1,1],
                   [-1,2,1],
                   [1,1,0]]
        tablero_visible = [['2',VACIO,'1'],[VACIO,'2','1'],['1','1','0']]
        self.assertTrue (todas_celdas_seguras_descubiertas (tablero,tablero_visible)) 

    def test_todas_celdas_seguras_cubiertas_False (self): 
        tablero = [[2,-1,1],
                   [-1,2,1],
                   [1,1,0]]
        tablero_visible = [[VACIO,VACIO,VACIO],[VACIO,VACIO,'1'],['1','1','0']]
        self.assertFalse (todas_celdas_seguras_descubiertas (tablero,tablero_visible))

class test_sacar_repetidos (unittest.TestCase): 
    def test_sacar_repetidos (self): 
        lista: list[list] = [[2,1],[2,1],[3,4],[5,2]]
        self.assertEqual (sacar_repetidos (lista), [[2,1],[3,4],[5,2]]) 

class test_buscador (unittest.TestCase): 
    def test_buscador_con_minas(self): 
        tablero = [[2,-1,1],
                   [-1,1,1],
                   [1,1,0]]
        self.assertEqual (buscador(tablero,2,2), [(1,2),(2,1),(1,1)])
    
class test_marcar_bombas_al_finalizar (unittest.TestCase): 
    def test_marcar_bombas_al_finalizar (self): 
        estado: EstadoJuego = {'filas': 3,'columnas': 3,'minas': 3,'tablero': [
                [2, -1, 1],
                [-1, 3, 1],
                [-1, 2, 0]],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]],
            'juego_terminado': False}
        
        descubrir_celda(estado, 0, 1)
        
        # Testeamos que se marquen las bombas
        self.assertEqual(estado['tablero_visible'], [[VACIO, BOMBA, VACIO],[BOMBA, VACIO, VACIO],[BOMBA, VACIO, VACIO]])
        # Testeamos que el juego se haya terminado 
        self.assertTrue(estado['juego_terminado'])

   
class descubrir_celdaTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {'filas': 3,'columnas': 3,'minas': 3,'tablero': [
                [2, -1, 1],
                [-1, 3, 1],
                [-1, 2, 0]],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]],
            'juego_terminado': False}
        
        descubrir_celda(estado, 2, 2)
        
        # Testeamos que la celda descubierta sea visible
        self.assertEqual(estado['tablero_visible'], [[VACIO, VACIO, VACIO],[VACIO, "3", "1"],[VACIO, "2", "0"]])
        
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 3)
        self.assertEqual(estado['tablero'], [[2, -1, 1],[-1, 3, 1],[-1, 2, 0]])

        # Testeamos que haya una mina en el tablero y no se haya terminado el juego
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 3)
        self.assertFalse(estado['juego_terminado'])

    def test_descubrir_celda_ultima (self):  
        estado: dict [str,Any] = {'filas' : 3, 'columnas' : 3, 'minas' : 1, 'tablero': [
            [0,1,-1],
            [0,1,1],
            [0,0,0]],
        'tablero_visible' : [
            ['0','1',VACIO],
            ['0','1','1'],
            [VACIO,'0','0']]}
        
        descubrir_celda (estado,2,0)
        
        self.assertEqual(estado['tablero_visible'],[['0','1',VACIO],['0','1','1'],['0','0','0']],) 
        self.assertTrue(estado['juego_terminado'])

    def test_descubrir_bomba_en_el_primer_intento (self): 
        estado: EstadoJuego = {'filas': 3,'columnas': 3,'minas': 3,'tablero': [
                [2, -1, 1],
                [-1, 3, 1],
                [-1, 2, 0]],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]],
            'juego_terminado': False}
        
        descubrir_celda(estado, 0, 1)
        
        # Testeamos que muestre las bombas ya que el usuario perdio
        self.assertEqual(estado['tablero_visible'], [[VACIO, BOMBA, VACIO],[BOMBA, VACIO, VACIO],[BOMBA, VACIO, VACIO]])
        
        #Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 3)
        self.assertEqual(estado['tablero'], [[2, -1, 1],[-1, 3, 1],[-1, 2, 0]])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 3)
        #  Testeamos que el juego haya terminado
        self.assertTrue(estado['juego_terminado'])
    
    def test_descubrir_una_sola_celda (self): 
        estado: EstadoJuego = {'filas': 3,'columnas': 3,'minas': 1,'tablero': [
                [-1, 1, 0],
                [1, 1, 0],
                [0, 0, 0]],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]],
            'juego_terminado': False}
        
        descubrir_celda(estado, 0, 1)
        
        # Testeamos que la celda descubierta sea visible
        self.assertEqual(estado['tablero_visible'], [[VACIO,'1', VACIO],[VACIO, VACIO, VACIO],[VACIO, VACIO, VACIO]])
        
        #Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [[-1, 1, 0],[1, 1, 0],[0, 0, 0]])
        
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertFalse(estado['juego_terminado'])

    def test_descubrir_ceros_verticales (self): 
        estado: EstadoJuego = {'filas': 3,'columnas': 3,'minas': 2,'tablero': [
                [-1, 1, 0],
                [2, 2, 0],
                [-1, 1, 0]],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]],
            'juego_terminado': False}
        
        descubrir_celda(estado, 0,2)
        
        # Testeamos que la celda descubierta sea visible
        self.assertEqual(estado['tablero_visible'], [[VACIO, '1', '0'],[VACIO, '2', '0'],[VACIO, '1', '0']])
        
        #Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [[-1, 1, 0],[2, 2, 0],[-1, 1, 0]])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 2)
        self.assertFalse(estado['juego_terminado'])

    def test_descubrir_ceros_diagonales (self): 
        estado: EstadoJuego = {'filas': 4,'columnas': 4,'minas': 2,'tablero': [
                [ 0, 0, 1, -1],
                [ 0, 0, 1, 1],
                [ 1, 1, 0, 0],
                [-1, 1, 0, 0]],
            'tablero_visible': [
                [VACIO, VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO, VACIO]
                ],
            'juego_terminado': False
            }
        
        descubrir_celda(estado, 1,1)
        
        # Testeamos que la celda descubierta sea visible
        self.assertEqual(estado['tablero_visible'],  [['0', '0', '1', VACIO], ['0', '0', '1', '1'], ['1', '1', '0', '0'],[VACIO, '1', '0', '0']])
        #Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 4)
        self.assertEqual(estado['columnas'], 4)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [[ 0, 0, 1, -1],[ 0, 0, 1, 1],[ 1, 1, 0, 0],[-1, 1, 0, 0]])
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 2)
        self.assertTrue(estado['juego_terminado'])

    def test_descubrir_ceros_horizontales (self): 
        estado: EstadoJuego = {'filas': 3,'columnas': 3,'minas': 2,'tablero': [
                [-1, 2, -1],
                [1, 2, 1],
                [0, 0, 0]],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]],
            'juego_terminado': False}
        
        descubrir_celda(estado, 2,0)
        
        # Testeamos que la celda descubierta sea visible
        self.assertEqual(estado['tablero_visible'], [[VACIO,VACIO, VACIO],['1', '2', '1'],['0', '0', '0']])
        
        #Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], [[-1, 2, -1],[1, 2, 1],[0, 0, 0]])
        
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 2)
        self.assertFalse(estado['juego_terminado'])

    def test_descubrir_numeros_y_no_bombas (self):
        # Testeamos si descubrimos todos los numeros y quedan solo las bombas sin descubrir  
        estado: EstadoJuego = {'filas' : 3, 'columnas' : 3, 'minas' : 1, 'tablero': [
            [0,1,-1],
            [0,1,1],
            [0,0,0]],
        'tablero_visible' : [
            ['0','1',VACIO],
            ['0','1','1'],
            [VACIO,'0','0']]}
        
        descubrir_celda (estado,2,0)
        
        self.assertEqual(estado['tablero_visible'],[['0','1',VACIO],['0','1','1'],['0','0','0']],) 
        self.assertTrue(estado['juego_terminado'])
        
" ------------------------------------ EJERCICIO 7 ------------------------------------------"

class verificar_victoriaTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {'filas': 2,'columnas': 2,'minas': 1,'tablero': [
                [-1, 1],
                [ 1, 1]],
            'tablero_visible': [
                [VACIO, "1"],
                ["1", "1"]],
            'juego_terminado': False}
        
        # Testeamos que el juego no esté terminado y que no haya ganado
        self.assertTrue(verificar_victoria(estado))
        
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [[-1, 1],[ 1, 1]])
        self.assertEqual(estado['tablero_visible'], [[VACIO, "1"],["1", "1"]])
        self.assertFalse(estado['juego_terminado'])
    
    def test_verificar_victoria_false(self):
        # testeamos que pasa devuelva victoria solo cuando corresponda
        estado: EstadoJuego = {'filas': 2,'columnas': 2,'minas': 1,'tablero': [
                [-1, 1],
                [ 1, 1]],
            'tablero_visible': [
                [VACIO, VACIO],
                ["1", "1"]],
            'juego_terminado': False}
        
        # Testeamos que el juego no esté terminado y que no haya ganado
        self.assertFalse(verificar_victoria(estado))
        
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [[-1, 1],[ 1, 1]])
        self.assertEqual(estado['tablero_visible'], [[VACIO, VACIO],["1", "1"]])
        self.assertFalse(estado['juego_terminado'])

class test_todas_celdas_seguras_descubiertas(unittest.TestCase):
    def test_todas_celdas_seguras_descubiertas_true(self):
        tablero = [[-1,1],[1,1]]
        tablero_visible = [[VACIO,"1"],["1","1"]]
        self.assertTrue(todas_celdas_seguras_descubiertas(tablero,tablero_visible))

    def test_todas_celdas_seguras_descubiertas_bandera(self):
        tablero = [[-1,1],[1,1]]
        tablero_visible = [[VACIO,BANDERA],["1","1"]]
        self.assertFalse(todas_celdas_seguras_descubiertas(tablero,tablero_visible))    

"------------------------------ EJERCICIO 8 -------------------------------------------------"

class reiniciar_juegoTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {'filas': 2,'columnas': 2,'minas': 1,'tablero': [
                [-1, 1],
                [ 1, 1]],
            'tablero_visible': [
                [VACIO, "1"],
                [VACIO, VACIO]],
            'juego_terminado': False}
        
        reiniciar_juego(estado)

        # Testeamos que el juego esté reiniciado
        self.assertEqual(estado['tablero_visible'], [[VACIO, VACIO],[VACIO, VACIO]])
        
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(len(estado['tablero']), 2)
        self.assertEqual(len(estado['tablero'][0]), 2)
        self.assertFalse(estado['juego_terminado'])

        # Testeamos que es diferente tablero
        self.assertNotEqual(estado['tablero'], [[-1, 1],[ 1, 1]])

    def test_juego_ganado(self):
        estado: EstadoJuego = {'filas': 2,'columnas': 2,'minas': 1,'tablero': [
                [-1, 1],
                [ 1, 1]],
            'tablero_visible': [
                [BANDERA, "1"],
                [VACIO, VACIO]],
            'juego_terminado': True}
        
        reiniciar_juego(estado)

        # Testeamos que el juego esté reiniciado
        self.assertEqual(estado['tablero_visible'], [[VACIO, VACIO],[VACIO, VACIO]])
        
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(len(estado['tablero']), 2)
        self.assertEqual(len(estado['tablero'][0]), 2)
        self.assertFalse(estado['juego_terminado'])

        # Testeamos que es diferente tablero
        self.assertNotEqual(estado['tablero'], [[-1, 1],[ 1, 1]])            

    def test_juego_perdido(self):
        estado: EstadoJuego = {'filas': 2,'columnas': 2,'minas': 1,'tablero': [
                [-1, 1],
                [ 1, 1]],
            'tablero_visible': [
                [BOMBA, "1"],
                [VACIO, VACIO]],
            'juego_terminado': True}
        
        reiniciar_juego(estado)

        # Testeamos que el juego esté reiniciado
        self.assertEqual(estado['tablero_visible'], [[VACIO, VACIO],[VACIO, VACIO]])
        
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(len(estado['tablero']), 2)
        self.assertEqual(len(estado['tablero'][0]), 2)
        self.assertFalse(estado['juego_terminado'])

        # Testeamos que es diferente tablero
        self.assertNotEqual(estado['tablero'], [[-1, 1],[ 1, 1]])  

    def test_juego_sin_terminar(self):
        estado: EstadoJuego = {'filas': 2,'columnas': 2,'minas': 1,'tablero': [
                [-1, 1],
                [ 1, 1]],
            'tablero_visible': [
                [VACIO, "1"],
                [VACIO, VACIO]],
            'juego_terminado': False}
        
        reiniciar_juego(estado)

        # Testeamos que el juego esté reiniciado
        self.assertEqual(estado['tablero_visible'], [[VACIO, VACIO],[VACIO, VACIO]])
        
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(len(estado['tablero']), 2)
        self.assertEqual(len(estado['tablero'][0]), 2)
        self.assertFalse(estado['juego_terminado'])

        # Testeamos que es diferente tablero
        self.assertNotEqual(estado['tablero'], [[-1, 1],[ 1, 1]])  


"------------------------------------ EJERCICIO 9 ----------------------------------------"   

#test1
estado_guardar: EstadoJuego = {'filas': 2,'columnas': 2,'minas': 1,'tablero': [
                    [-1, 1],
                    [ 1, 1]],
                'tablero_visible': [
                    [BANDERA, "1"],
                    [VACIO, VACIO]],
                'juego_terminado': False}

#test2
estado_guardar2: EstadoJuego = {'filas': 4,'columnas': 4,'minas': 1,'tablero': [
                    [-1, 1, 0, 0],
                    [ 1, 1, 0, 0],
                    [ 0, 0, 0, 0],
                    [ 0, 0, 0, 0]],
                'tablero_visible': [
                    [VACIO, "1", VACIO, VACIO],
                    [VACIO, VACIO, VACIO, VACIO],
                    [VACIO, VACIO, VACIO, VACIO],
                    [VACIO, VACIO, VACIO, VACIO]],
                'juego_terminado': False}

#test3
estado_guardar3: EstadoJuego = {'filas': 2,'columnas': 2,'minas': 4,'tablero': [
                    [-1, -1],
                    [-1, -1]],
                'tablero_visible': [
                    [VACIO, VACIO],
                    [VACIO, VACIO]],
                'juego_terminado': False}

#test4
estado_guardar4: EstadoJuego = {'filas': 2,'columnas': 2,'minas': 1,'tablero': [
                    [0,0],
                    [0,0]],
                'tablero_visible': [
                    [VACIO, VACIO],
                    [VACIO, VACIO]],
                'juego_terminado': False} 

class guardar_estadoTest(unittest.TestCase):
    
    def test_chico (self):
         # Testea que se guarda correctamente un tablero chico
        resultado_esperado_visible: list[str] = ["*,1\n",'?,?\n']
        resultado_esperado_oculto: list[str] = ['-1,1\n','1,1\n']

        guardar_estado (estado_guardar, './save/casoTest1(Guardar)/') 

        #abro los archivos que se guardaron y leo sus lineas
        archivo1 = open ('./save/casoTest1(Guardar)/tablero.txt',"r", encoding= "UTF-8")
        resultado_obtenido_oculto: list [str] = archivo1.readlines ()
        archivo1.close()

        archivo2 = open ('./save/casoTest1(Guardar)/tablero_visible.txt',"r", encoding= "UTF-8")
        resultado_obtenido_visible: list [str] = archivo2.readlines ()
        archivo2.close()
        
        self.assertEqual(resultado_esperado_visible, resultado_obtenido_visible)
        self.assertEqual(resultado_esperado_oculto, resultado_obtenido_oculto)

    def test_grande (self):
         # Testea que se guarda correctamente un tablero grande
        resultado_esperado_visible: list[str] = ['?,1,?,?\n','?,?,?,?\n','?,?,?,?\n','?,?,?,?\n']
        resultado_esperado_oculto: list[str] = ['-1,1,0,0\n','1,1,0,0\n','0,0,0,0\n','0,0,0,0\n']
        
        guardar_estado (estado_guardar2, './save/casoTest2(Guardar)/') 

        #abro los archivos que se guardaron y leo sus lineas
        archivo1 = open ('./save/casoTest2(Guardar)/tablero.txt',"r", encoding= "UTF-8")
        resultado_obtenido_oculto: list [str] = archivo1.readlines ()
        archivo1.close()

        archivo2 = open ('./save/casoTest2(Guardar)/tablero_visible.txt',"r", encoding= "UTF-8")
        resultado_obtenido_visible: list [str] = archivo2.readlines ()
        archivo2.close()

        self.assertEqual(resultado_esperado_visible, resultado_obtenido_visible)
        self.assertEqual(resultado_esperado_oculto, resultado_obtenido_oculto)
    
    def test_full_bomba (self):
         # Testea que se guarda correctamente un tablero con todas bombas
        resultado_esperado_visible: list[str] = ['?,?\n','?,?\n']
        resultado_esperado_oculto: list[str] = ['-1,-1\n','-1,-1\n']
        
        guardar_estado (estado_guardar3, './save/casoTest3(Guardar)/') 

        #abro los archivos que se guardaron y leo sus lineas
        archivo1 = open ('./save/casoTest3(Guardar)/tablero.txt',"r", encoding= "UTF-8")
        resultado_obtenido_oculto: list [str] = archivo1.readlines ()
        archivo1.close()

        archivo2 = open ('./save/casoTest3(Guardar)/tablero_visible.txt',"r", encoding= "UTF-8")
        resultado_obtenido_visible: list [str] = archivo2.readlines ()
        archivo2.close()

        self.assertEqual(resultado_esperado_visible, resultado_obtenido_visible)
        self.assertEqual(resultado_esperado_oculto, resultado_obtenido_oculto)

    def test_sin_bomba (self):
         # Testea que se guarda correctamente un tablero sin bombas
        resultado_esperado_visible: list[str] = ['?,?\n','?,?\n']
        resultado_esperado_oculto: list[str] = ['0,0\n','0,0\n']
        
        guardar_estado (estado_guardar4, './save/casoTest4(Guardar)/') 

        #abro los archivos que se guardaron y leo sus lineas
        archivo1 = open ('./save/casoTest4(Guardar)/tablero.txt',"r", encoding= "UTF-8")
        resultado_obtenido_oculto: list [str] = archivo1.readlines ()
        archivo1.close()

        archivo2 = open ('./save/casoTest4(Guardar)/tablero_visible.txt',"r", encoding= "UTF-8")
        resultado_obtenido_visible: list [str] = archivo2.readlines ()
        archivo2.close()

        self.assertEqual(resultado_esperado_visible, resultado_obtenido_visible)
        self.assertEqual(resultado_esperado_oculto, resultado_obtenido_oculto)

"------------------------------------ EJERCICIO 10 ----------------------------------------" 

#referencia para cargar_estado:
estado_absurdo: EstadoJuego = {"filas" : 50, "columnas" : 15, "minas" : 150, "tablero" : [
        [1,7],
        [8,0]], 
    "tablero_visible" : [
        [' ','1'],
        ['1','1']],
        "juego_terminado" : False}

class test_comas_en_lista(unittest.TestCase):
    def test_comas_validas(self):
        #todo correcto
        resultado_esperado: dict[str, Any] = {"comas" : 2, "comas_validas" : True, "misma_cantidad" : True}
        resultado_obtenido: dict[str, Any] = comas_en_lista(['1,1,1'])
        self.assertEqual(resultado_esperado, resultado_obtenido)

    def test_comas_invalidas_ensub1_1(self):
        #no hay numero antes de la coma.
        resultado_esperado: dict[str, Any] = {"comas" : 1, "comas_validas" : False, "misma_cantidad" : True}
        resultado_obtenido: dict[str, Any] = comas_en_lista(['1,'])
        self.assertEqual(resultado_esperado, resultado_obtenido)

    def test_comas_invalidas_ensub1_2(self):
        #no hay numero en medio de unas comas.
        resultado_esperado: dict[str, Any] = {"comas" : 2, "comas_validas" : False, "misma_cantidad" : True}
        resultado_obtenido: dict[str, Any] = comas_en_lista(['1,,1'])
        self.assertEqual(resultado_esperado, resultado_obtenido)

    def test_comas_invalidas_ensub2(self):
        #distintas cantidades de comas.
        resultado_esperado: dict[str, Any] = {"comas" : 2, "comas_validas" : True, "misma_cantidad" : False}
        resultado_obtenido: dict[str, Any] = comas_en_lista(['1,2,3', '1,2'])
        self.assertEqual(resultado_esperado, resultado_obtenido)

class test_eliminar_saltos(unittest.TestCase):
    def test_quitar_saltos(self):
        #quita los saltos correctamente.
        resultado_esperado: list[str] = ['1,1','1,1']
        resultado_obtenido: list[str] = eliminar_saltos(['1,1\n','1,1\n'])
        self.assertEqual(resultado_esperado, resultado_obtenido)

class cargar_estadoTest(unittest.TestCase):
    def test_carga_positiva (self):
        #este recorre practicamente todo el codigo, solo con este bastaria para minimo un 90% de cobertura.
        valor_esperado: bool = True
        valor_obtenido: bool = cargar_estado(estado_absurdo,"./save/casoTest1(True)/")
        self.assertEqual(valor_esperado, valor_obtenido)
    
    def test_error_en_condicion1(self):
        #no encuentra uno de los archivos.
        valor_esperado: bool = False
        valor_obtenido: bool = cargar_estado(estado_absurdo, "./save/casoTest2(False)")
        self.assertEqual(valor_esperado, valor_obtenido)

    def test_error_en_condicion2(self):
        #no tienen la misma cantidad de filas.
        valor_esperado: bool = False
        valor_obtenido: bool = cargar_estado(estado_absurdo, "./save/casoTest3(False)")
        self.assertEqual(valor_esperado, valor_obtenido)
         
    def test_error_en_condicion3(self):
        #no tienen la misma cantidad de comas.
        valor_esperado: bool = False
        valor_obtenido: bool = cargar_estado(estado_absurdo, "./save/casoTest4(False)")
        self.assertEqual(valor_esperado, valor_obtenido)

    def test_error_en_condicion4sub1(self):
        #no hay minas en tablero.
        valor_esperado: bool = False
        valor_obtenido: bool = cargar_estado(estado_absurdo,  "./save/casoTest5(False)")
        self.assertEqual(valor_esperado, valor_obtenido)
    
    def test_error_en_condicion4sub2(self):
        #los valores adyacentes a minas son validos.
        valor_esperado: bool = False
        valor_obtenido: bool = cargar_estado(estado_absurdo, "./save/casoTest6(False)")
        self.assertEqual(valor_esperado, valor_obtenido)
    
    def test_error_en_condicion5sub1(self):
        #hay un elemento distinto de los admitidos.
        valor_esperado: bool = False
        valor_obtenido: bool = cargar_estado(estado_absurdo, "./save/casoTest7(False)")
        self.assertEqual(valor_esperado, valor_obtenido)

    def test_error_en_condicion5sub2(self):
        #los numeros en tablero visible no coinciden con el tablero oculto.
        valor_esperado: bool = False
        valor_obtenido: bool = cargar_estado(estado_absurdo, "./save/casoTest8(False)")
        self.assertEqual(valor_esperado, valor_obtenido)
    
    def test_error_en_condicion6sub1(self):
        #no hay ningun vacio.
        valor_esperado: bool = False
        valor_obtenido: bool = cargar_estado(estado_absurdo, "./save/casoTest9(False)")
        self.assertEqual(valor_obtenido, valor_esperado)

    def test_error_en_condicion7sub1(self):
        #no se puede armar una matriz con los tableros.
        valor_esperado: bool = False
        valor_obtenido: bool = cargar_estado(estado_absurdo, "./save/casoTest11(False)")
        self.assertEqual(valor_esperado, valor_obtenido)

    def test_error_en_condicion7sub2(self):
        #las lineas no tienen la misma cantidad de comas(columnas)
        valor_esperado: bool = False
        valor_obtenido: bool = cargar_estado(estado_absurdo, "./save/casoTest12(False)")
        self.assertEqual(valor_esperado, valor_obtenido)

if __name__ == '__main__':
    unittest.main(verbosity=2) # pragma: no cover