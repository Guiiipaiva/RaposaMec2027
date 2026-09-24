from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ColorSensor
from pybricks.parameters import Port, Button
from pybricks.tools import wait

hub = PrimeHub()
sensor = ColorSensor(Port.A)

sensor.lights.on(20)

def calibrar_prata():

    h_min = 360
    h_max = 0

    s_min = 100
    s_max = 0

    v_min = 100
    v_max = 0

    print("CALIBRACAO DO PRATA")
    print("Aperte o botao esquerdo")

    # Espera o botão esquerdo
    while Button.LEFT not in hub.buttons.pressed():
        wait(50)

    print("Comecando em 3 segundos...")
    wait(3000)

    print("CALIBRANDO...")

    tempo = 0

    while tempo < 3000:

        # HSV
        H, S, V = sensor.hsv()

        h_min = min(h_min, H)
        h_max = max(h_max, H)

        s_min = min(s_min, S)
        s_max = max(s_max, S)

        v_min = min(v_min, V)
        v_max = max(v_max, V)
        
        wait(50)
        tempo += 50

    print("CALIBRACAO TERMINADA!")

    return (
        h_min, h_max,
        s_min, s_max,
        v_min, v_max,
    )

(
    h_min, h_max,
    s_min, s_max,
    v_min, v_max,
) = calibrar_prata()

print("H:", h_min, "-", h_max)
print("S:", s_min, "-", s_max)
print("V:", v_min, "-", v_max)

# SALVAR NO STORAGE

dados = bytes([

    h_min // 256,
    h_min % 256,

    h_max // 256,
    h_max % 256,

    s_min,
    s_max,

    v_min,
    v_max,

])


hub.system.storage(0, write=dados)


print("CALIBRACAO SALVA!")
