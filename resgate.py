from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from pybricks.messaging import BLERadio

hub = PrimeHub()

sensor_prata = ColorSensor(Port.A)

sensor_prata.lights.on(20)

radio = BLERadio(broadcast_channel=61)

motor_garra = Motor(Port.B, Direction.COUNTERCLOCKWISE)
motor_cesto = Motor(Port.D, Direction.COUNTERCLOCKWISE)

def subir_garra():
    motor_garra.run_time(500, 600)

def descer_garra():
        motor_garra.run_time(-500, 600)

def descarregar():
    motor_cesto.run_time(600, 500)

def voltar_cesto():
    motor_cesto.run_time(-600, 500)

def carregar_calibracao():

    dados = hub.system.storage(0, read=10)

    h_min = dados[0] * 256 + dados[1]
    h_max = dados[2] * 256 + dados[3]

    s_min = dados[4]
    s_max = dados[5]

    v_min = dados[6]
    v_max = dados[7]

    ref_min = dados[8]
    ref_max = dados[9]

    return (
        h_min, h_max,
        s_min, s_max,
        v_min, v_max,
    )


MARGEM_H = 4
MARGEM_S = 2
MARGEM_V = 2

def prata(sensor):

    H, S, V = sensor.hsv()

    reflexo = sensor.reflection()

    if (h_min - MARGEM_H <= H <= h_max + MARGEM_H and
        s_min - MARGEM_S <= S <= s_max + MARGEM_S and
        v_min - MARGEM_V <= V <= v_max + MARGEM_V ):

        return True

    return False

def manda_mensagem():

    if prata(sensor_prata):

        radio.broadcast("PRATA")

    else:

        radio.broadcast("NADA")

(
    h_min, h_max,
    s_min, s_max,
    v_min, v_max,
) = carregar_calibracao()

print("CALIBRACAO CARREGADA!")

print("H:", h_min, "-", h_max)
print("S:", s_min, "-", s_max)
print("V:", v_min, "-", v_max)

while True:

    manda_mensagem()

    wait(100)