from piezas import Torre, Peon, Alfil, Reina, Rey, Caballo, configuracion_inicial




def imprimir_tablero(tablero):
    print("\n" + "_" * 22 + "\n")
    numero = "87654321"  # Filas, es al reves para que se acomode mejor la vista del jugador blanco que es el que empieza
    contador = 0
    for fila in reversed(tablero):  # Invertimos las filas para que queden abajo las blancas
        print(numero[contador], ' '.join(str(elemento) for elemento in fila))  # las columnas siguen iguales
        contador += 1
    print("  A B C D E F G H" + "\n" + "_" * 22)  # Letras de columnas


# Creamos el tablero inicial

tablero_vacio = []

for i in range(8):
    if i % 2 == 0:
        tablero_vacio.append(["□", "■"] * 4)
    else:
        tablero_vacio.append(["■", "□"] * 4)



tablero_inicial = tablero_vacio.copy() # Empiezas con las casillas vacías

for (fila, col), pieza in configuracion_inicial.items():
    tablero_inicial[fila][col] = pieza # Asignas el objeto directamente




