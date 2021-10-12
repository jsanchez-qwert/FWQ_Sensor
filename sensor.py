"""
    TODO majear las señales de sistema para la interrupcion del bucle infinito
"""
import random
import re
import time
from sys import argv

from kafka import KafkaProducer


class Sensor:
    def __init__(self, ip_servidor: str, puerto: int, id: str):
        """
        Inicializa el sensor de la atraccion que le digas
        :param ip_servidor: ip del setvidor de kafka
        :param puerto: puerto del servidor de kafka
        :param id: identificador de la atraccion
        """
        self.p_cola = 20
        self.ip = ip_servidor
        self.puerto = puerto
        self.id = id
        self.producer = KafkaProducer(bootstrap_servers=f'{self.ip}:{self.puerto}')

    def close(self):
        self.producer.close()

    def run(self):
        """
        Envia cada 1-3 segundo cuantas personas hay en la atraccion
        :return:
        """
        while True:
            time.sleep(random.randint(1, 3))
            mensaje = str(self.id).encode() + b' ' + str(self.p_cola).encode()
            print(mensaje)
            self.producer.send("atracciones", mensaje)
            self.p_cola += abs(random.randint(-4, 4))


def filtra(args: list) -> bool:
    """
    Indica si el formato de los argumentos es el correcto
    :param args:
    :return:
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


if __name__ == '__main__':
    if not filtra(argv):
        print("ERROR: Argumentos incorrectos")
        print("Usage: sensor.py <ip_servidor:puerto> <id> ")
        print("Example: sensor.py 192.168.56.33:9092 02")
        exit()

    ip = argv[1].split(':')[0]
    port = int(argv[1].split(':')[1])
    atraccion = argv[2]
    try:
        s = Sensor(ip, port, atraccion)
        s.run()
    except Exception as e:
        print("ERROR: ", e)
    finally:
        s.close()
