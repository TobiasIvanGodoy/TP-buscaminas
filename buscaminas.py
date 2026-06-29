import random
from typing import Any, TextIO
import os

# Constantes para dibujar
BOMBA = chr(128163)  # simbolo de una mina
BANDERA = chr(128681)  # simbolo de bandera blanca
VACIO = " "  # simbolo vacio inicial

# Tipo de alias para el estado del juego
EstadoJuego = dict[str, Any]

def existe_archivo(ruta_directorio: str, nombre_archivo:str) -> bool:
    """Chequea si existe el archivo en la ruta dada"""
    return os.path.exists(os.path.join(ruta_directorio, nombre_archivo))

"""---------------------------- Ejercicio 1 ----------------------------"""

def generador_de_matriz(filas:int,columnas:int)->list[list[int]]:
    """Genera una matriz de filas x columnas, con 0 en cada posicion
    Args:
        filas:entero que representa las filas de la matriz.
        columnas: entero que representa las columnas de la matriz.
    Returns:
        Matriz de tamaño fila x columna
        """
    res:list[list[int]] = []
    f:int = filas
    while f>0:
        res.append([])
        f-=1
    for j in res:
        c = 0
        while c<columnas:
            j.append(0)
            c+=1
    return res

def colocar_minas(filas:int, columnas: int, minas:int) -> list[list[int]]:
    """Genera una matriz de 0 con minas(-1) en posiciones aleatorias.
    Args:
        filas: la cantidad de filas que tendra la matriz.
        columna: la cantidad de columnas que tendra la matriz.
        minas: la cantidad de minas(-1) que tendra la matriz.
    Returns:
        La matriz de (fila x columna) tiene solo el numero de minas dado y 0.
    """
    res:list[list[int]] = generador_de_matriz(filas,columnas)#le pido a la otra funcion una matriz/tablero de 0
    m:int = minas 
    lista_filas_y_columnas:list[int] = range(0,filas*columnas)
    posiciones:list[int] = random.sample(lista_filas_y_columnas,minas)
    for posicion in posiciones:
        num_celda = 0
        for fila in range(len(res)):
            for celda in range(len(res[0])):
                if num_celda == posicion:
                    res[fila][celda] = -1
                num_celda+=1
    return res

"""---------------------------- Ejercicio 2 ----------------------------"""

def en_rango(tablero:list[list[int]],f:int,c:int)->bool:
    """Comprueba si las 'coordenadas' dadas estan dentro del tablero.
    Args:
        tablero: matriz con valores entre -1 y 8 
        f: numero de coordenada en la fila 
        c: numero coordenada en la columna 
    Returns:
        True: si f esta entre 0 y la cantidad de las listas -1 y c esta entre 0 y la longitud de filas -1
        """
    res:bool = False
    if 0 <= f < len(tablero) and 0 <= c < len(tablero[0]):
        res = True
    return res

def buscador_de_minas(tablero:list[list[int]])->list[tuple[int,int]]:
    """Guarda en una lista por cada mina la fila y columna en forma de dupla.
    Args:
        tablero: es una matriz con valores entre -1 y 8 inclusive.
    Returns:
        Devuelve las coordenadas donde hay minas en forma de una lista de duplas talque (fila,columna).
    """
    minas:list[tuple[int,int]] = []
    for fila in range(len(tablero)):
        for columna in range(len(tablero[0])):
            celda:int = tablero[fila][columna]
            if celda == -1:
                minas.append((fila,columna))
    return minas

def calcular_numeros(tablero: list[list[int]]) -> None:
    """Reemplaza los ceros que corresponde por el numero de minas que tiene alrededor. Para ello busca las minas y luego recorre la lista con las posiciones de las minas y suma 1 en cada direccion posible. Al final convierte las coordenadas de las minas de vuelta en minas por si fueron modificadas.
    Args:
        tablero: matriz con valores entre -1 y 8 inclusive.
    Returns:
        No retorna nada, solo modifica el tablero con los numeros actualizados.
    """
    minas:list[tuple[int,int]] = buscador_de_minas(tablero)
    direcciones:list[tuple[int,int]] = [(-1,0),(1,0),(0,1),(0,-1),(-1,1),(1,1),(-1,-1),(1,-1)]
    for fila,columna in minas:
        for df,dc in direcciones:
            if en_rango(tablero,fila+df,columna+dc) == True:
                tablero[fila+df][columna+dc] +=1
    for fila,columna in minas:
        tablero[fila][columna] = -1

"""---------------------------- Ejercicio 3 ----------------------------"""

def crear_juego(filas:int, columnas:int, minas:int) -> EstadoJuego:
    """Inicia un Juego, dados los parametros filas, columnas y minas genera un tablero.
    Args:
        filas: cant filas que tendra la matriz.
        columnas: cant columnas que tendra la matriz.
        minas: cant minas que tendra la matriz.
    Returns:
        Genera un estado de juego con un tablero de las dimensiones pedidas, un tablero_visible con todos VACIO, guarda con claves de igual 
        nombre los parametros de entrada y una clave llamada juego_terminado = False.
    """
    tablero:list[list[int]] = (colocar_minas(filas,columnas,minas))
    calcular_numeros(tablero)
    tablero_visible = []
    for fila in range(len(tablero)):
        tablero_visible.append([])
        for columna in range(len(tablero[0])):
            tablero_visible[fila].append(VACIO)
    res:EstadoJuego = {}
    res["filas"] = filas
    res["columnas"] = columnas
    res["minas"] = minas
    res["tablero"] = tablero
    res["tablero_visible"] = tablero_visible
    res["juego_terminado"] = False
    return res

"""---------------------------- Ejercicio 4 ----------------------------"""

def obtener_estado_tablero_visible(estado: EstadoJuego) -> list[list[str]]:
    """Dado el estado de juego, devuelve el tablero visible.
    Args:
        estado: diccionario con las claves filas, columnas, minas, tablero, tablero_visible y juego_terminado.
    Returns:
        Devuelve el valor que este cargado en la clave 'tablero_visible'.
        """
    mostrarTablero: list[list[str]] = estado['tablero_visible']
    tablero_copia: list[list[str]] = []
    for i in range(len(mostrarTablero)):
        fila: list[str] = []
        for j in range(len(mostrarTablero[i])):
            fila.append(mostrarTablero[i][j])
        tablero_copia.append(fila)
    return tablero_copia

"""---------------------------- Ejercicio 5 ----------------------------"""

def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    """ Dada la posicion(fila x columna) de una celda modifica el tablero visible de VACIO a BANDERA o de BANDERA a VACIO.
    Args:
        estado: diccionario con claves: filas, columnas, minas, tablero, tablero_visible y juego_terminado.
        fila: entero mayor a -1 y menor a estado['filas']
        columna: entero mayor a -1 y menor a estado['columnas']
    Returns:
        Nada, modifica el valor de la clave tablero_visble del estado dado."""
    marcada_en_turno: bool = False
    if not estado["juego_terminado"]:
        tablero_visible:list[list[str]] = estado["tablero_visible"]
        if tablero_visible[fila][columna] == VACIO:
            tablero_visible[fila][columna] = BANDERA
            marcada_en_turno = True
        if tablero_visible[fila][columna] == BANDERA and not marcada_en_turno:  
            tablero_visible[fila][columna] = VACIO

"""---------------------------- Ejercicio 6 ----------------------------"""

def todas_celdas_seguras_descubiertas(tablero:list[list[int]],tablero_visible:list[list[str]])->bool:# chequea 
    """ Comprueba si las celdas que en tablero son un numero >=0 estan descubiertas en tablero_visible.
    Args:
        tablero: Es una matriz con numeros entre -1 y 8 inclusive. 
        tablero_visible: Es una matriz de igual dimension a tablero, que puede contener VACIO,BANDERA, BOMBA o un numero entre 0 y 8.
    Returns:
        True si para cada celda de tablero que es mayor o igual a 0 el mismo valor se observa en tablero_visible.
    """
    
    res:bool = True 
    for num_de_fila in range(len(tablero)):
        fila:list[int] = tablero[num_de_fila]
        for num_de_columna in range(len(fila)):
            celda:int = tablero[num_de_fila][num_de_columna]
            celda_visible = tablero_visible[num_de_fila][num_de_columna]
            if celda >= 0 and celda_visible == VACIO:
                res = False
            if celda != -1 and celda_visible == BANDERA:
                res = False  
    return res

def sacar_repetidos(lista:list)->list:
    """Dada una lista elimina los objetos repetidos, dejando uno solo
    Args:
        lista: lista de elementos
    Returns:
        Una nueva lista de longitud menor o igual a la original, con los elementos de lista, pero sin repetirlos."""
    res:list = []
    for elemento in lista:
        if elemento not in res:
            res.append(elemento)
    return res

def buscador_de_ceros_en_circulo(tablero:list[list[int]],fila:int,columna:int,visitados:list[tuple[int,int]])->list[tuple[int,int]]:
    """Dado un tablero y una posicion(fila x columna) genera una lista con todas las posiciones alrededor y comprueba su valor.
    Si son distintos a 0 los guarda en una lista final, si son cero los guarda en una lista auxiliar y se llama si misma, y repite el proceso.
    Para evitar que repita infinitamente guarda la posicion de las celdas que ya llamo en la lista visitados.
    Args:
        tablero: matriz con numeros de -1 a 8 inclusive.
        fila: enteros con rango de 0 a longitud de tablero-1.
        columna: enteros con rango de 0 a longitud de tablero-1.
        visitados: lista de tuplas que contiene la coordenadas de los que ya fueron revisados. 
    Returns:
        Lista de posiciones de la matriz.
    """
    res:list[tuple[int,int]] = []
    res_aux:list[tuple[int,int]] = []
    celda:int = tablero[fila][columna]
    direcciones:list[tuple[int,int]] = [(-1,1),(1,1),(-1,-1),(1,-1),(1,0),(-1,0),(0,1),(0,-1)]
    if (fila,columna) in visitados:
        return []
    else:
        visitados.append((fila,columna))
    for direccion_fila,direccion_col in direcciones:
        f_alt = fila + direccion_fila
        c_alt = columna + direccion_col
        if en_rango(tablero,f_alt,c_alt) == True and tablero[f_alt][c_alt] == 0:
            res_aux.append((f_alt,c_alt))
        elif en_rango(tablero,f_alt,c_alt) == True and tablero[f_alt][c_alt] != 0:
            res.append((f_alt,c_alt))
    for celda in res_aux:
        res += buscador_de_ceros_en_circulo(tablero,celda[0],celda[1],visitados)
    sacar_repetidos(res_aux)
    res+=res_aux
    return res

def buscador(tablero:list[list[int]],fila:int,columna:int)->list[tuple[int,int]]:
    """Busca las posiciones de las celdas adyacentes hasta armar un perimetro de celdas que no son ceros.
    Args:
        tablero: matriz compuesta por enteros del -1 al 8 inclusive.
        fila: numero entero mayor o igual a 0 y menor a la longitud de tablero.
        columna: numero entero mayor o igual a 0 y menor a la longitud de una fila.
    Returns:
        Todas las celdas adyacentes que sean mayores o iguales a 0, en forma de dupla(fila x columna) """
    res:list[tuple[int,int]] = []
    visitados:list[tuple[int,int]] = []
    num_fila:int = fila
    num_col:int = columna
    celda = tablero[fila][columna]
    if celda != 0:
        res = [(fila,columna)]
    else:
        direcciones = [(1,0),(-1,0),(0,1),(0,-1),(-1,1),(1,1),(-1,-1),(1,-1)]
        for dir_fila,dir_col in direcciones:
            num_fila+=dir_fila
            num_col+=dir_col
            if en_rango(tablero,num_fila,num_col) and tablero[num_fila][num_col] == 0:
                res+= buscador_de_ceros_en_circulo(tablero,num_fila,num_col,visitados)
            elif en_rango(tablero,num_fila,num_col) and tablero[num_fila][num_col] > 0:
                res.append((num_fila, num_col))
            num_fila = fila
            num_col = columna
        res = sacar_repetidos(res)
    return res

def marcar_bombas_al_finalizar(estado:EstadoJuego,fila:int,columna:int)->None:
    """Marca todas las bombas.
    Args:
        estado: diccionario con las claves filas, columnas, minas, tablero, tablero_visible y juego_terminado.
        fila: num entero entre 0 y estado[filas]
        columna: num entero entre 0 y estado[columnas]
    Returns:
        Nada, cambia el tablero visible"""
    for num_fila in range(len(estado["tablero"])):
        for num_col in range(len(estado["tablero"][num_fila])):
            if estado["tablero"][num_fila][num_col] == -1:
                estado["tablero_visible"][num_fila][num_col] = BOMBA

def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    """Dado una celda y un estado revela los valores que corresponde, si es una bomba todas las bombas y termina el juego, si es un num mayor a 0 entonces solo revela esa, si es un cero revela los 0 y numeros adyacentes hasta formar un perimetro de numeros.
    Args:
        estado: diccionario con las claves filas, columnas, minas, tablero, tablero_visible y juego_terminado.
        fila: num entero entre 0 y estado[filas]
        columna: num entero entre 0 y estado[columnas]
    Returns:
        Vacio, solo modifica el tablero_visible dentro de estado
        """
    celda_og:int = estado["tablero"][fila][columna]
    if celda_og == -1:# si encuentra una bomma desbloquea todas las bombas
        estado["tablero_visible"][fila][columna] = BOMBA
        estado["juego_terminado"] = True
        marcar_bombas_al_finalizar(estado,fila,columna)
    else:
        estado["tablero_visible"][fila][columna] = str(celda_og)
        celdas_para_desbloquear:list[tuple[int,int]] = buscador(estado["tablero"],fila,columna)
        for f,c in celdas_para_desbloquear:
            estado["tablero_visible"][f][c] = str(estado["tablero"][f][c])
        if todas_celdas_seguras_descubiertas(estado["tablero"],estado["tablero_visible"]) == True:
            estado["juego_terminado"] = True

"""---------------------------- Ejercicio 7 ----------------------------"""

def verificar_victoria(estado: EstadoJuego) -> bool:
    """Comprueba si la partida esta ganada, usando todas_celdas_seguras_descubiertas.
    Args:
        estado: diccionario con las claves filas, columnas, minas, tablero, tablero_visible y juego_terminado.
    Returns:
        True si solo si todas las celdas seguras fueron decubiertas."""
    tablero: list[list[int]] = estado["tablero"]
    tableroVisible: list[list[str]] = estado["tablero_visible"] 
    return todas_celdas_seguras_descubiertas(tablero,tableroVisible)

"""---------------------------- Ejercicio 8 ----------------------------"""

def reiniciar_juego(estado: EstadoJuego) -> None:
    """Comienza una nueva partida con un nuevo tablero, pero las mismas dimensiones y misma cantidad de minas.
    Args:
        estado: un diccionario con las claves filas, columnas, minas, tablero, tablero_visible y juego_terminado
    Returns:
        Vacio, solo modifica el tablero y vuelve el tablero_visible a VACIO."""
    tablero_original:list[list[int]] = estado["tablero"]
    filas:int = estado["filas"]
    columnas:int = estado["columnas"]
    minas:int = estado["minas"]
    estado_nuevo:dict = crear_juego(filas,columnas,minas)
    tablero_nuevo:list[list[int]] = estado_nuevo["tablero"]
    while tablero_nuevo == tablero_original:
        tablero_nuevo = colocar_minas(filas,columnas,minas)
        calcular_numeros(tablero_nuevo)
    estado["tablero"] = tablero_nuevo
    estado["tablero_visible"] = estado_nuevo["tablero_visible"]
    estado["juego_terminado"] = False


"""---------------------------- Ejercicio 9 ----------------------------"""

def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    """Permite guardar en un archivo de texto una partida sin terminar. Para ello guarda el tablero y el tablero visible.
    Args:
        estado: el diccionario con las claves: filas, columnas, minas, tablero, tablero_visible y juego_terminado.
        ruta_directorio: donde se guardara el archivo con la partida.
    Returns:
        Vacio, no retorna nada"""
    tablero_visible_guardado: TextIO = open(ruta_directorio + "/tablero_visible.txt", "w", encoding="UTF-8") #abro los archivos o lo creo si no existen.
    tablero_guardado = open(ruta_directorio + "/tablero.txt", "w", encoding="UTF-8") 
    tablero_visible = estado["tablero_visible"] #llamo a los tableros del diccionario estado.
    tablero = estado["tablero"] 
    for i in range(len(tablero)): #recorro el tablero y voy metiendo las filas en strings.
        linea_tablero = "" 
        for j in range(len(tablero[0])):
            linea_tablero += str(tablero[i][j])
            if j < len(tablero[0]) - 1: #agrego comas entre espacios de los valores
                linea_tablero += ","
        tablero_guardado.write(linea_tablero + "\n") #agrego al archivo la fila con un salto de linea.
    for i in range(len(tablero_visible)): #hago lo mismo con el tablero visible.
        linea_visible = ""
        for j in range(len(tablero_visible[0])):
            celda = tablero_visible[i][j]
            if celda == VACIO:
                linea_visible += "?"
            elif celda == BANDERA:
                linea_visible += "*"
            else:
                linea_visible += str(celda)
            if j < len(tablero_visible[0]) - 1:
                linea_visible += ","
        tablero_visible_guardado.write(linea_visible + "\n")

    tablero_guardado.close()
    tablero_visible_guardado.close()

"""---------------------------- Ejercicio 10 ---------------------------"""

def comas_en_lista(tablero: list[str]) -> dict[str, Any]:
    """Comprueba la cantidad de comas (,) en una lista, y verifica que el resto tengan la misma cantidad. Ademas comprueba que sean validas.
    Args:
        tab: lista de strings.
    Returns:
        diccionario con la cantidad de comas, si las posiciones de las comas son validas y si tiene la misma cantidad de comas"""
    res: dict[str, Any] = {}
    comas_validas: bool = True
    cantidad_comas: list[int] = []
    misma_cantidad: bool = True
    
    for linea in tablero:
        comas: int = 0
        numero_actual: str = ""
        for caracter in linea:
            if caracter == ",":
                if numero_actual == "":
                    comas_validas = False
                else:
                    numero_actual = ""
                comas += 1
            else:
                numero_actual += caracter
        cantidad_comas.append(comas)
        if numero_actual == "":
            comas_validas = False
    
    for i in cantidad_comas:
        if i != cantidad_comas[0]:
            misma_cantidad = False
    
    res["comas"] = cantidad_comas[0]
    res["comas_validas"] = comas_validas
    res["misma_cantidad"] = misma_cantidad

    return res

def generar_tablero(lineastab: list[str], esInt: bool) -> list[list[Any]]:
    """Genera un tablero donde guardar las lineas y su contenido.
    Args:
        lineastab: listas de strings que representan el tablero.
        esInt: indica si los valores deben convertirse a enteros o mantenerse como strings.
    Returns:
        Lista de listas de enteros o strings, es decir la matriz/tablero con los valores correspondientes."""
    tablero_real: list[list[Any]] = []

    for linea in lineastab:
        linea_actual: list[Any] = [] 
        numero_actual: str = ""
        for caracter in linea:
            if caracter == ",":
                if esInt == True:
                    linea_actual.append(int(numero_actual))
                else:
                    linea_actual.append(numero_actual)
                numero_actual = ""
            else:
                numero_actual += caracter

        if esInt == True:
            linea_actual.append(int(numero_actual))
        else:
            linea_actual.append(numero_actual)
        tablero_real.append(linea_actual)

    return tablero_real

def eliminar_saltos(tab:list[str])->list[str]:
    """Elimina los saltos de linea de listas de string.
    Args:
        tab: listas de string.
    Returns:
        La misma lista pero sin los saltos de linea."""
    tablero_final: list [str] = []
    linea_actual: str = ""
    for linea in tab:
        for celda in linea:
            if celda != "\n":
                linea_actual += celda
        tablero_final.append(linea_actual)
        linea_actual = ""
    return tablero_final

def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
    """Dado un estado y una ubicacion, carga la partida guardada en esa ubicacion.
    Args:
        estado: diccionario con las claves filas, columnas, minas, tablero, tablero_visible y juego_teminado.
        ruta_directorio: string con donde esta guardado el estado.
    Returns:
        True si solo si la ruta_directorio lleva a un archivo con formato correcto y reemplaza el actual."""
    
    #verifico en cada paso que el archivo siga siendo válido, sino salta al final del programa.
    valido: bool = True 

    #ASEGURA 1:

    #condicion 1: compruebo que los archivos existan.

    if ruta_directorio[-1] != "/":
        ruta_directorio = ruta_directorio + "/"
        
    if (not existe_archivo(ruta_directorio, "tablero.txt")) or (not existe_archivo(ruta_directorio, "tablero_visible.txt")):
        valido = False
    
    #condicion 2: la cantidad de lineas en tablero.txt es igual a la cantidad de lineas en tablero_visible.txt
    if valido:
        tablero_abierto: TextIO = open(ruta_directorio + "tablero.txt", "r", encoding="UTF-8")
        tab: list[str] = eliminar_saltos(tablero_abierto.readlines())
        tablero_abierto.close()

        tablero_visible_abierto: TextIO = open(ruta_directorio + "tablero_visible.txt", "r", encoding="UTF-8")
        tab_visible : list[str] = eliminar_saltos(tablero_visible_abierto.readlines())
        tablero_visible_abierto.close()
        
        if len(tab) != len(tab_visible):
            valido = False

    #condicion 3: tablero.txt y tablero_visible.txt contienen la misma cantidad de (",")
    if valido:
        if comas_en_lista(tab)["comas"] != comas_en_lista(tab_visible)["comas"]:
            valido = False
    
    #condicion 4: en tablero.txt hay almenos una mina y las posiciones adyacentes a una mina cumplen con la especificacion.

    if valido:
        tablero_real : list[list[int]]= generar_tablero(tab, True)
        tablero_real_copia: list[list[int]] = generar_tablero(tab, True)

        contador_de_minas: int = 0
        for linea in tablero_real:
            for celda in linea:
                if celda == -1:
                    contador_de_minas += 1
        
        if contador_de_minas == 0:
            valido = False
    
    if valido:
        for indice in range(len(tablero_real_copia)):
            for posicion in range(len(tablero_real_copia[indice])):
                if tablero_real_copia[indice][posicion] != -1:
                    tablero_real_copia[indice][posicion] = 0

        calcular_numeros(tablero_real_copia)
        
        if tablero_real != tablero_real_copia:
            valido = False

    #condicion 5.1: en tablero_visible.txt solo hay numeros entre [0;8], "*", "?", y ","

    if valido:
        valores_validos: str = "012345678,*?"

        for linea in tab_visible:
            for caracter in linea:
                if caracter not in valores_validos:
                    valido = False
    
    #condicion 5.2: los numeros en tablero visible son iguales a los numeros en tablero.

    if valido:
        tab_visible_real: list[list[str]] = generar_tablero(tab_visible, False)

        contador_de_vacios: int = 0 

        for indice in range(len(tab_visible_real)):
            for posicion in range(len(tab_visible_real[indice])):
                if tab_visible_real[indice][posicion] in "012345678" and not tab_visible_real[indice][posicion] == '':
                    if int(tab_visible_real[indice][posicion]) != tablero_real[indice][posicion]:
                        valido = False
                if tab_visible_real[indice][posicion] == "?":
                    contador_de_vacios += 1

    #condicion 6: en tablero_visible.txt debe haber almenos un "?"

    if valido:
        if contador_de_vacios == 0:
            valido = False
    
    #condicion 7: todos los valores en tablero y tablero_visible estan separados por comas, de forma tal que se puede representar una matriz con ambos tableros.

    if valido:
        for t in [tab, tab_visible]:
            if not comas_en_lista(t)["misma_cantidad"] or not comas_en_lista(t)["comas_validas"]:
                valido = False

    #ASEGURA 2: cargo todos los valores en el diccionario.

    #transformo los * en banderas y los ? en vacios.
    if valido: 
        for indice in range(len(tab_visible_real)):
            for posicion in range(len(tab_visible_real[indice])):
                if tab_visible_real[indice][posicion] == "*":
                    tab_visible_real[indice][posicion] = BANDERA
                elif tab_visible_real[indice][posicion] == "?":
                    tab_visible_real[indice][posicion] = VACIO

        estado.clear()

        estado["minas"] = contador_de_minas
        estado["juego_terminado"] = False
        estado["tablero"] = tablero_real
        estado["tablero_visible"] = tab_visible_real
        estado["filas"] = len(tablero_real)
        estado["columnas"] = (comas_en_lista(tab)["comas"])+1

    return valido