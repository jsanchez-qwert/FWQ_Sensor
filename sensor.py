import random
import re
import signal
import time
from sys import argv

from kafka import KafkaProducer

COLA_INICIAL = 20


def run(productor: KafkaProducer) -> None:
    """
    Envia cada 1-3 segundo cuantas personas hay en la atraccion
    """
    interrupted = False
    p_cola = COLA_INICIAL
    while running:
        mensaje = str(atraccion).encode() + b' ' + str(p_cola).encode()
        print(mensaje)
        productor.send("atracciones", mensaje)
        p_cola += abs(random.randint(-4, 4))
        time.sleep(random.randint(1, 3))


def filtra(args: list) -> bool:
    """
    Indica si el formato de los argumentos es el correcto
    :param args: Argumentos del programa
    """
    if len(argv) != 3:
        print("Numero incorrecto de argumentos")
        return False

    regex_1 = '^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{1,5}$'
    regex_2 = '^\S+:[0-9]{1,5}$'
    if not (re.match(regex_1, args[1]) or re.match(regex_2, args[1])):
        print("Direccion incorrecta")
        return False
    return True


def signal_handler(sig, frame):
    """
    Maneja la flag de final para terminal el bucle infinito cuando se le manda SIGINT
    """
    global running
    print("TERMINANDO PROCESO DE SENSOR")
    running = False


if __name__ == '__main__':
    if not filtra(argv):
        print("ERROR: Argumentos incorrectos")
        print("Usage: sensor.py <ip_servidor:puerto> <id> ")
        print("Example: sensor.py 192.168.56.33:9092 02")
        exit()

    ip = argv[1].split(':')[0]
    port = int(argv[1].split(':')[1])
    atraccion = argv[2]

    signal.signal(signal.SIGINT, signal_handler)
    running = True
    try:
        producer = KafkaProducer(bootstrap_servers=f'{ip}:{port}')
        run(producer)
    except Exception as e:
        print("ERROR: ", e)
    finally:
        if 'producer' in locals():
            producer.close()
    exit(0)
