import pickle


def codificar(msg: bytearray) -> bytearray:
    """Codifica un mensaje encriptado"""
    mensaje_final = bytearray()
    largo = len(msg).to_bytes(4, "little")
    mensaje_final += bytearray(largo)
    chunks_completos = len(msg) // 128
    cantidad_faltante = len(msg) % 128
    for i in range(0, chunks_completos):
        numero_bloque_bytes = i.to_bytes(4, "big")
        posicion_inicial = i * 128
        posicion_final = (i * 128) + 128
        bloque = msg[posicion_inicial:posicion_final]
        mensaje_final += bytearray(numero_bloque_bytes)
        mensaje_final += bloque

    if cantidad_faltante != 0:  # hay un chunk incompleto
        numero_bloque = chunks_completos
        numero_bloque_bytes = numero_bloque.to_bytes(4, "big")
        posicion_inicial = numero_bloque * 128
        posicion_final = (numero_bloque * 128) + cantidad_faltante
        bloque = msg[posicion_inicial:posicion_final]
        mensaje_final += bytearray(numero_bloque_bytes)
        mensaje_final += bloque
        for i in range(cantidad_faltante, 128):
            mensaje_final += bytearray(b'\x00')
    return mensaje_final


def decodificar(msg: bytearray) -> bytearray:
    """Decodifica un mensaje coficicado"""
    mensaje_preliminar = bytearray()
    largo = decodificar_largo(msg)
    mensaje = msg[4:]
    lista_bytes = [mensaje[i:i+132] for i in range(0, len(mensaje), 132)]
    for chunk in lista_bytes:
        sub_chunk = chunk[4:]  # ignora datos
        mensaje_preliminar += sub_chunk

    mensaje_decodificado = mensaje_preliminar[:largo]  # ignorar \x00
    return mensaje_decodificado


def decodificar_largo(mensaje: bytearray) -> int:
    bytes_largo = mensaje[0:4]
    return int.from_bytes(bytes_largo, byteorder="little")


def serializar(objeto: object) -> bytearray:
    """Serializa el elemento con pickle
     y retorna un bytearray del mismo"""
    return bytearray(pickle.dumps(objeto))


def deserializar(elemento: bytearray) -> object:
    """Deserealiza el bytearray con pickle"""
    return pickle.loads(elemento)
