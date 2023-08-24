def encriptar(msg: bytearray, N: int) -> bytearray:
    """Retorna el bytearray encriptado"""
    copia = msg.copy()
    for i in range(len(msg)):
        copia[(i + N) % len(msg)] = msg[i]
    backup_pos_n = copia[(N) % len(msg)]
    backup_pos_inicial = copia[0]
    copia[0] = backup_pos_n
    copia[(N) % len(msg)] = backup_pos_inicial
    return copia


def desencriptar(msg: bytearray, N: int) -> bytearray:
    """Retorna el bytearray desencriptado"""
    copia = msg.copy()
    buffer = msg[(N) % len(msg)]
    buffer_2 = msg[0]
    msg[0] = buffer
    msg[(N) % len(msg)] = buffer_2

    for i in range(len(msg)):
        copia[i] = msg[(i + N) % len(msg)]
    return copia


if __name__ == "__main__":
    # Testear encriptar
    N = 1
    msg_original = bytearray(b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x00\x01\x02\x03\x04\x05')
    msg_esperado = bytearray(b'\x01\x05\x02\x03\x04\x05\x06\x07\x08\x09\x00\x01\x02\x03\x04')
    msg_encriptado = encriptar(msg_original, N)
    if msg_encriptado != msg_esperado:
        print("[ERROR] Mensaje escriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje escriptado correctamente")
    
    # Testear desencriptar
    msg_desencriptado = desencriptar(msg_esperado, N)
    if msg_desencriptado != msg_original:
        print("[ERROR] Mensaje descencriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje descencriptado correctamente")
