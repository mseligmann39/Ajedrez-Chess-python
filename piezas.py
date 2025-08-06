class Pieza:
    
    def __init__(self, color):
        self.color = color
        
    def __str__(self):
        return ' '

    def es_movimiento_valido(self, origen, destino,tablero):
        raise NotImplementedError("Este método debe ser implementado por las subclases")
    
class Peon(Pieza):
    
    # En piezas.py, en la clase Peon

    def es_movimiento_valido(self, origen, destino, tablero):
        fila_origen, col_origen = origen
        fila_destino, col_destino = destino
        direccion = 1 if self.color == 'blanco' else -1

        # --- INTENCIÓN 1: AVANZAR (la columna es la misma) ---
        if col_origen == col_destino:
            
            # A) Movimiento de 1 paso
            if fila_destino == fila_origen + direccion:
                # CONDICIÓN: La casilla de destino DEBE estar vacía.
                if not isinstance(tablero[fila_destino][col_destino], Pieza):
                    return True

            # B) Movimiento de 2 pasos
            elif fila_destino == fila_origen + 2 * direccion:
                # CONDICIÓN 1: El peón debe estar en su fila de inicio específica.
                es_fila_inicio = (self.color == 'blanco' and fila_origen == 1) or \
                                (self.color == 'negro' and fila_origen == 6)
                
                if es_fila_inicio:
                    # CONDICIÓN 2 y 3: La casilla intermedia Y la de destino deben estar vacías.
                    casilla_intermedia = tablero[fila_origen + direccion][col_origen]
                    casilla_destino = tablero[fila_destino][col_destino]
                    if not isinstance(casilla_intermedia, Pieza) and not isinstance(casilla_destino, Pieza):
                        return True
    
        # --- INTENCIÓN 2: CAPTURAR (la columna cambia en 1) ---
        elif abs(col_origen - col_destino) == 1 and fila_destino == fila_origen + direccion:
            pieza_a_capturar = tablero[fila_destino][col_destino]
            # CONDICIÓN: Debe haber una pieza ENEMIGA en el destino.
            if isinstance(pieza_a_capturar, Pieza) and pieza_a_capturar.color != self.color:
                return True

        # Si ninguna de las condiciones anteriores devolvió True, el movimiento es inválido.
        return False
    
    def __init__(self, color):
        super().__init__(color)

    def obtener_simbolo(self):
        return "♙" if self.color == "blanco" else "♟"

    def __str__(self):
        return self.obtener_simbolo()

class Torre(Pieza):
    
    def es_movimiento_valido(self, origen, destino,tablero):
        fila_origen, col_origen = origen
        fila_destino, col_destino = destino
        if fila_origen != fila_destino and col_origen != col_destino:
            return False
        # Verificar si hay piezas en el camino
        elif fila_origen == fila_destino:

            for col in range(min(col_origen, col_destino) + 1, max(col_origen, col_destino)):
                if isinstance(tablero[fila_origen][col], Pieza):
                    return False
                
        elif col_origen == col_destino:
        # Lógica similar a la horizontal, pero para las filas
            for fila in range(min(fila_origen, fila_destino) + 1, max(fila_origen, fila_destino)):
                if isinstance(tablero[fila][col_origen], Pieza):
                    return False  # Camino bloqueado
                
        pieza_destino = tablero[fila_destino][col_destino]

        if isinstance(pieza_destino, Pieza) and pieza_destino.color == self.color:
            return False
        # Si no hay bloqueos, el movimiento es válido
        return True  # Movimiento válido
    
    def __init__(self, color):
        super().__init__(color)

    def obtener_simbolo(self):
        return "♖" if self.color == "blanco" else "♜"

    def __str__(self):
        return self.obtener_simbolo()

class Caballo(Pieza):
    
    def es_movimiento_valido(self, origen, destino, tablero):
        fila_origen, col_origen = origen
        fila_destino, col_destino = destino

        # 1. Comprobar la forma del movimiento en "L"
        delta_fila = abs(fila_origen - fila_destino)
        delta_col = abs(col_origen - col_destino)

        es_movimiento_L = (delta_fila == 1 and delta_col == 2) or \
                        (delta_fila == 2 and delta_col == 1)

        if not es_movimiento_L:
            return False

        # ¡NO HAY BUCLE PARA COMPROBAR EL CAMINO!

        # 2. Comprobar la casilla de destino (lógica idéntica a las otras)
        pieza_en_destino = tablero[fila_destino][col_destino]
        if isinstance(pieza_en_destino, Pieza) and pieza_en_destino.color == self.color:
            return False

        return True

    def __init__(self, color):
        super().__init__(color)

    def obtener_simbolo(self):
        return "♘" if self.color == "blanco" else "♞"

    def __str__(self):
        return self.obtener_simbolo()

class Alfil(Pieza):
    
    def es_movimiento_valido(self, origen, destino, tablero):
        fila_origen, col_origen = origen
        fila_destino, col_destino = destino
        
        if abs(fila_origen - fila_destino) != abs(col_origen - col_destino):
            return False
        # Verificar si hay piezas en el camino
        fila_direccion = 1 if fila_destino > fila_origen else -1   
        col_direccion = 1 if col_destino > col_origen else -1 
        fila_actual = fila_origen + fila_direccion
        col_actual = col_origen + col_direccion 
        while (fila_actual != fila_destino) and (col_actual != col_destino):
            if isinstance(tablero[fila_actual][col_actual], Pieza):
                return False
            fila_actual += fila_direccion
            col_actual += col_direccion
        pieza_destino = tablero[fila_destino][col_destino]
        if isinstance(pieza_destino, Pieza) and pieza_destino.color == self.color:
            return False
        return True

    def __init__(self, color):
        super().__init__(color)

    def obtener_simbolo(self):
        return "♗" if self.color == "blanco" else "♝"

    def __str__(self):
        return self.obtener_simbolo()

class Reina(Pieza):
    def es_movimiento_valido(self, origen, destino, tablero):
        fila_origen, col_origen = origen
        fila_destino, col_destino = destino

        # 1. Comprobar la forma del movimiento
        es_recto = (fila_origen == fila_destino or col_origen == col_destino)
        es_diagonal = (abs(fila_origen - fila_destino) == abs(col_origen - col_destino))

        if not (es_recto or es_diagonal):
            return False # No es un movimiento válido para una reina

        # 2. Comprobar el camino
        if es_recto:
            # Aquí va la lógica de camino que usaste para la TORRE
            if fila_origen == fila_destino:

                for col in range(min(col_origen, col_destino) + 1, max(col_origen, col_destino)):
                    if isinstance(tablero[fila_origen][col], Pieza):
                        return False
                
            elif col_origen == col_destino:
            # Lógica similar a la horizontal, pero para las filas
                for fila in range(min(fila_origen, fila_destino) + 1, max(fila_origen, fila_destino)):
                    if isinstance(tablero[fila][col_origen], Pieza):
                        return False  # Camino bloqueado
        elif es_diagonal:
            fila_direccion = 1 if fila_destino > fila_origen else -1   
            col_direccion = 1 if col_destino > col_origen else -1 
            fila_actual = fila_origen + fila_direccion
            col_actual = col_origen + col_direccion 
            while (fila_actual != fila_destino) and (col_actual != col_destino):
                if isinstance(tablero[fila_actual][col_actual], Pieza):
                    return False
                fila_actual += fila_direccion
                col_actual += col_direccion
                # Aquí va la lógica de camino que usaste para el ALFIL


        # 3. Comprobar la casilla de destino (es la misma lógica para todos)
        pieza_en_destino = tablero[fila_destino][col_destino]
        if isinstance(pieza_en_destino, Pieza) and pieza_en_destino.color == self.color:
            return False

        return True
    
    def __init__(self, color):
        super().__init__(color)

    def obtener_simbolo(self):
        return "♕" if self.color == "blanco" else "♛"

    def __str__(self):
        return self.obtener_simbolo()

class Rey(Pieza):

    def es_movimiento_valido(self, origen, destino, tablero):
        fila_origen, col_origen = origen
        fila_destino, col_destino = destino

        # 1. Comprobar la distancia del movimiento
        delta_fila = abs(fila_origen - fila_destino)
        delta_col = abs(col_origen - col_destino)

        # El rey se mueve un máximo de 1 casilla en cualquier dirección
        if delta_fila > 1 or delta_col > 1:
            return False

        # 2. Comprobar la casilla de destino (lógica idéntica a las otras)
        pieza_en_destino = tablero[fila_destino][col_destino]
        if isinstance(pieza_en_destino, Pieza) and pieza_en_destino.color == self.color:
            return False

        return True

    def __init__(self, color):
        super().__init__(color)

    def obtener_simbolo(self):
        return "♔" if self.color == "blanco" else "♚"

    def __str__(self):
        return self.obtener_simbolo()
    

configuracion_inicial = {
    # Piezas Blancas
    (0, 0): Torre("blanco"), (0, 1): Caballo("blanco"), (0, 2): Alfil("blanco"), (0, 3): Reina("blanco"),
    (0, 4): Rey("blanco"), (0, 5): Alfil("blanco"), (0, 6): Caballo("blanco"), (0, 7): Torre("blanco"),
    (1, 0): Peon("blanco"), (1, 1): Peon("blanco"), (1, 2): Peon("blanco"), (1, 3): Peon("blanco"),
    (1, 4): Peon("blanco"), (1, 5): Peon("blanco"), (1, 6): Peon("blanco"), (1, 7): Peon("blanco"),

    # Piezas Negras (¡complétalas tú!)
    (6, 0): Peon("negro"), (6, 1): Peon("negro"),(6, 2): Peon("negro"), (6, 3): Peon("negro"),
     (6, 4): Peon("negro"), (6, 5): Peon("negro"),(6, 6): Peon("negro"), (6, 7): Peon("negro"), # ... etc.
    (7, 0): Torre("negro"), (7, 1): Caballo("negro"),(7,2): Alfil("negro"),(7,3): Reina("negro"),
     (7,4): Rey("negro"), (7,5): Alfil("negro"), (7,6): Caballo("negro"), (7,7): Torre("negro") # ... etc.
}

