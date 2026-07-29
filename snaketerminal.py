import os
import sys
import time
import random
 
os.system("")
 
#condicional para definir funciones para simular fluidez en la terminal, llamando librerías como msvcrt para Windows y termios tty y select para linux
if os.name == "nt":
    import msvcrt
 
    def teclapresionada():
        if msvcrt.kbhit():
            tecla = msvcrt.getch()
 
            if tecla == b"\xe0":
                tecla2 = msvcrt.getch()
                flechas = {
                    b"H": "ARRIBA",
                    b"P": "ABAJO",
                    b"K": "IZQUIERDA",
                    b"M": "DERECHA",
                }
                return flechas.get(tecla2, None)
 
            if tecla == b"\r":
                return "ENTER"
            if tecla == b"\x1b":
                return "ESC"
 
            try:
                letra = tecla.decode().lower()
            except Exception:
                return None
 
            letras = {"w": "ARRIBA", "s": "ABAJO", "a": "IZQUIERDA", "d": "DERECHA"}
            return letras.get(letra, None)
 
        return None
 
    def prepararteclado():
        pass  
 
    def restaurarteclado():
        pass  
 
else:
    import termios
    import tty
    import select
 
    configuracionoriginalterminal = None
 
    def prepararteclado():
        global configuracionoriginalterminal
        descriptor = sys.stdin.fileno()
        configuracionoriginalterminal = termios.tcgetattr(descriptor)
        tty.setcbreak(descriptor)
 
    def restaurarteclado():
        descriptor = sys.stdin.fileno()
        termios.tcsetattr(
            descriptor, termios.TCSADRAIN, configuracionoriginalterminal
        )
 
    def teclapresionada():
        haydatos, _, _ = select.select([sys.stdin], [], [], 0)
        if not haydatos:
            return None
 
        tecla = sys.stdin.read(1)
 
        if tecla == "\x1b":
            haymas, _, _ = select.select([sys.stdin], [], [], 0.01)
            if haymas:
                resto = sys.stdin.read(2)
                flechas = {
                    "[A": "ARRIBA",
                    "[B": "ABAJO",
                    "[D": "IZQUIERDA",
                    "[C": "DERECHA",
                }
                return flechas.get(resto, None)
            return "ESC"
 
        if tecla in ("\r", "\n"):
            return "ENTER"
 
        letras = {"w": "ARRIBA", "s": "ABAJO", "a": "IZQUIERDA", "d": "DERECHA"}
        return letras.get(tecla.lower(), None)
 
 
def esperartecla():
    while True:
        tecla = teclapresionada()
        if tecla == "ENTER" or tecla == "ESC":
            return tecla
        time.sleep(0.03)
 
 
def limpiarpantalla():
    print("\033[H", end="")
 
 
def ocultarcursor():
    print("\033[?25l", end="")
 
 
def mostrarcursor():
    print("\033[?25h", end="")
 
 
def limpiarconsolaunavez():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
 
 
mapa1 = [
    "########################################",
    "#                                      #",
    "#                                      #",
    "#                                      #",
    "#                                      #",
    "#                                      #",
    "#                                      #",
    "#                                      #",
    "#                                      #",
    "#                                      #",
    "#                                      #",
    "#                                      #",
    "#                                      #",
    "#                                      #",
    "#                                      #",
    "#                                      #",
    "########################################",
]
 
mapa2 = [
    "########################################",
    "#                                      #",
    "#                                      #",
    "#         ######            ######     #",
    "#                                      #",
    "#                                      #",
    "#      ##########      划分########       #",
    "#                                      #",
    "#                                      #",
    "#                                      #",
    "#      #########       #########       #",
    "#                                      #",
    "#                                      #",
    "#         ######            ######     #",
    "#                                      #",
    "#                                      #",
    "########################################",
]
 
MAPAS = [mapa1, mapa2]
 
 
def generarcomida(mapa, serpiente):
    while True:
        fila = random.randint(1, len(mapa) - 2)
        columna = random.randint(1, len(mapa[0]) - 2)
 
        espared = mapa[fila][columna] == "#"
        estaenserpiente = (fila, columna) in serpiente
 
        if not espared and not estaenserpiente:
            return (fila, columna)
 
 
def posicioninicial(mapa):
    return (5, 10)
 
 
def construirpantalla(mapa, serpiente, comida, puntaje):
    filasdibujo = []
    for filatexto in mapa:
        filasdibujo.append(list(filatexto))
 
    filacomida, columnacomida = comida
    filasdibujo[filacomida][columnacomida] = "*"
 
    for indice in range(len(serpiente)):
        fila, columna = serpiente[indice]
        if indice == 0:
            filasdibujo[fila][columna] = "0"
        else:
            filasdibujo[fila][columna] = "o"
 
    lineas = []
    lineas.append("Puntaje: " + str(puntaje) + "   (ESC para salir)")
    lineas.append("")
    for filalista in filasdibujo:
        lineas.append("".join(filalista))
 
    return lineas
 
 
def imprimirpantalla(lineas):
    limpiarpantalla()
    for linea in lineas:
        print(linea.ljust(60))
 
 
def jugar(mapa):    
    filainicial, columnainicial = posicioninicial(mapa)
 
    serpiente = [
        (filainicial, columnainicial),
        (filainicial, columnainicial - 1),
        (filainicial, columnainicial - 2),
    ]
 
    direccion = "DERECHA"
    comida = generarcomida(mapa, serpiente)
    puntaje = 0
    velocidad = 0.15  
 
    limpiarconsolaunavez()
    ocultarcursor()
 
    while True:
        tecla = teclapresionada()
 
        if tecla == "ESC":
            mostrarcursor()
            return puntaje
        elif tecla == "ARRIBA" and direccion != "ABAJO":
            direccion = "ARRIBA"
        elif tecla == "ABAJO" and direccion != "ARRIBA":
            direccion = "ABAJO"
        elif tecla == "IZQUIERDA" and direccion != "DERECHA":
            direccion = "IZQUIERDA"
        elif tecla == "DERECHA" and direccion != "IZQUIERDA":
            direccion = "DERECHA"
 
        cabezafila, cabezacolumna = serpiente[0]
 
        if direccion == "ARRIBA":
            nuevacabeza = (cabezafila - 1, cabezacolumna)
        elif direccion == "ABAJO":
            nuevacabeza = (cabezafila + 1, cabezacolumna)
        elif direccion == "IZQUIERDA":
            nuevacabeza = (cabezafila, cabezacolumna - 1)
        else:  
            nuevacabeza = (cabezafila, cabezacolumna + 1)
 
        nuevafila, nuevacolumna = nuevacabeza
        chocopared = mapa[nuevafila][nuevacolumna] == "#"
        chococuerpo = nuevacabeza in serpiente
 
        if chocopared or chococuerpo:
            mostrarcursor()
            return puntaje
 
        serpiente.insert(0, nuevacabeza)
 
        if nuevacabeza == comida:
            puntaje += 1
            comida = generarcomida(mapa, serpiente)
            if puntaje % 5 == 0 and velocidad > 0.06:
                velocidad -= 0.01  
        else:
            serpiente.pop()  
 
        lineas = construirpantalla(mapa, serpiente, comida, puntaje)
        imprimirpantalla(lineas)
 
        time.sleep(velocidad)
 
 
def mostrarmenu():
    limpiarconsolaunavez()
    print("=========================================")
    print("            JUEGO DE LA SERPIENTE          ")
    print("=========================================")
    print()
    print("Presiona ENTER para jugar")
    print("Presiona ESC para salir")
    print()
    print("Controles: W A S D")
 
    tecla = esperartecla()
    return tecla == "ENTER"
 
 
def mostrargameover(puntaje):
    limpiarconsolaunavez()
    print("=========================================")
    print("                 GAME OVER                  ")
    print("=========================================")
    print()
    print("Puntaje final:", puntaje)
    print()
    print("Presiona ENTER para reintentar")
    print("Presiona ESC para salir")
 
    tecla = esperartecla()
    return tecla == "ENTER"
 
 
def main():
    prepararteclado()
    try:
        while True:
            quierejugar = mostrarmenu()
            if not quierejugar:
                break
 
            mapa = random.choice(MAPAS)
            puntajefinal = jugar(mapa)
 
            quierereintentar = mostrargameover(puntajefinal)
            if not quierereintentar:
                break
    finally:
        restaurarteclado()
        mostrarcursor()
        limpiarconsolaunavez()
        print("Gracias por jugar!")
 
main()