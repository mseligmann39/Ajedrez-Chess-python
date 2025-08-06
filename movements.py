from piezas import Pieza, Peon, Torre, Alfil, Reina, Rey, Caballo
import copy


def traducir_movimiento(movimiento_str):

    if len(movimiento_str) != 4:
        raise ValueError("El formato de la jugada debe ser de 4 caracteres (ej: e2e4).")

    columnas = "abcdefgh"
    columna_inicio = columnas.find(movimiento_str[0])
    fila_inicio = int(movimiento_str[1]) - 1
    columna_destino = columnas.find(movimiento_str[2])
    fila_destino = int(movimiento_str[3]) - 1

    return (fila_inicio, columna_inicio), (fila_destino, columna_destino)


def realizar_movimiento(tablero, coords_origen, coords_destino, turno_actual):

    fila_origen, col_origen = coords_origen
    fila_destino, col_destino = coords_destino

    pieza_a_mover = tablero[fila_origen][col_origen]

    if isinstance(pieza_a_mover, Pieza):
        if pieza_a_mover.color != turno_actual:
            raise ValueError("No es tu turno para mover esta pieza.")

        elif pieza_a_mover.es_movimiento_valido(coords_origen, coords_destino, tablero):

            tablero_copy = copy.deepcopy(tablero)
            pieza_a_mover = tablero_copy[coords_origen[0]][coords_origen[1]]
            tablero_copy[fila_destino][col_destino] = pieza_a_mover
            tablero_copy[fila_origen][col_origen] = (
                "□" if (fila_origen + col_origen) % 2 == 0 else "■"
            )
            if hay_jaque(tablero_copy, turno_actual):
                raise ValueError("Movimiento ilegal: tu rey quedaría en jaque.")

            else:
                nuevo_turno = "negro" if turno_actual == "blanco" else "blanco"
                return tablero_copy, nuevo_turno
    else:
        raise ValueError("No hay una pieza en la posición de origen.")

    return tablero, turno_actual


def buscar_rey(tablero, color_del_rey):

    # Buscar la casilla del color del rey
    for fila in range(8):
        for columna in range(8):
            casillero_rey = tablero[fila][columna]
            if isinstance(casillero_rey, Rey):
                if casillero_rey.color == color_del_rey:
                    return (fila, columna)


def hay_jaque(tablero, color_rey):

    coords_rey = buscar_rey(tablero, color_rey)

    color_enemigo = "negro" if color_rey == "blanco" else "blanco"

    for fila in range(8):
        for columna in range(8):
            casilla = tablero[fila][columna]
            if isinstance(casilla, Pieza) and casilla.color == color_enemigo:
                prueba = casilla.es_movimiento_valido(
                    (fila, columna), coords_rey, tablero
                )
                if prueba:
                    return True

    return False


def traducir_movimiento_contrario(cords_origen,cords_destino):
    letras = "ABCDEFGH"
    
    return f'{letras[cords_origen[1]]}{cords_origen[0] + 1}{letras[cords_destino[1]]}{cords_destino[0] + 1 }'

def generar_movimientos_legales(tablero,color):

    movimientos_legales = []

    

    for fila_origen in range(8):
        for columna_origen in range(8):
            pieza_a_mover = tablero[fila_origen][columna_origen]
            if isinstance(pieza_a_mover,Pieza) and pieza_a_mover.color == color: 
                for fila_destino in range(8):
                    for columna_destino in range(8):
                        cords_origen = fila_origen,columna_origen
                        cords_destino = fila_destino,columna_destino
                        if pieza_a_mover.es_movimiento_valido(cords_origen,cords_destino,tablero):
                            
                            tablero_copy = copy.deepcopy(tablero)
                            tablero_copy[fila_destino][columna_destino] = pieza_a_mover
                            tablero_copy[fila_origen][columna_origen] = (
                                "□" if (fila_origen + columna_origen) % 2 == 0 else "■"
                            )
                            if not hay_jaque(tablero_copy, color):
                                movimiento = traducir_movimiento_contrario(cords_origen,cords_destino)
                                movimientos_legales.append(movimiento)
    return movimientos_legales
                            
                                


