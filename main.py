from tablero import imprimir_tablero, tablero_inicial
from movements import (
    traducir_movimiento,
    realizar_movimiento,
    hay_jaque,
    generar_movimientos_legales,
    traducir_movimiento_contrario
)
import re

turno_actual = "blanco"
print("Bienvenido al juego de ajedrez!")
print(
    "Las piezas se mueven usando el formato 'e2e4' (columna fila de origen a columna fila de destino)."
)
print("Escribe 'salir' para terminar el juego.")

jaque_mate = False

tablero_parcial = tablero_inicial.copy()

while not jaque_mate:
      # Copia del tablero actual para mostrar
    imprimir_tablero(tablero_parcial)
    patron = r"^[a-h][1-8][a-h][1-8]$"
    print(f"Turno del jugador {turno_actual}. Introduce tu jugada:")
    movimiento_str = input("Introduce tu jugada (ej: e2e4) o escribe 'salir': ")

    movimiento_str = movimiento_str.strip().lower()

    if not re.match(patron, movimiento_str) and movimiento_str != "salir":
        print("Formato de jugada inválido. Debe ser como 'e2e4'.")
        continue

    if movimiento_str == "salir":
        break

    try:
        coords_origen, coords_destino = traducir_movimiento(movimiento_str)
        print(f"Traducción: de {coords_origen} a {coords_destino}")
        tablero_parcial, turno_actual = realizar_movimiento(
            tablero_parcial, coords_origen, coords_destino, turno_actual
        )
        if hay_jaque(tablero_parcial, turno_actual):
            resultado = generar_movimientos_legales(tablero_parcial, turno_actual)
            if resultado == []:
                print(f"JAQUE MATE, REY EN JAQUE: {turno_actual}")
                break

    except (ValueError, IndexError) as e:
        print(f"Error: {e}")

turno_actual = "negro" if turno_actual == "blanco" else "blanco"
tablero_final = tablero_parcial
imprimir_tablero(tablero_final)
print(f"JAQUE MATE, GANADOR: Rey {turno_actual}")
