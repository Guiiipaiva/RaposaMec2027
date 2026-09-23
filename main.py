from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction, Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from pybricks.messaging import BLERadio

# 1. Inicializa o Hub
hub = PrimeHub()
radio = BLERadio(observe_channels=[61])
# 2. Configura os Motores da Esteira
motor_esquerdo = Motor(Port.A, Direction.COUNTERCLOCKWISE)
motor_direito = Motor(Port.B, Direction.CLOCKWISE)

anguloX, anguloY = hub.imu.tilt()
# 3. Configura a DriveBase
robo = DriveBase(motor_esquerdo, motor_direito, wheel_diameter=56, axle_track=112)

# 4. Configura os Sensores nas suas portas
sensor_esquerdo = ColorSensor(Port.C)
sensor_direito = ColorSensor(Port.D)
ultrasonicoFrente = UltrasonicSensor(Port.F)
ultrasonicoLado = UltrasonicSensor(Port.E)

ultrasonicoFrente.lights.off()
ultrasonicoLado.lights.off()

sensor_direito.lights.off()
sensor_esquerdo.lights.off() 

KP = 7
POTENCIA_BASE = 70
KD = 0.8

erro_anterior = 0  

def PID():
    global erro_anterior
    anguloX, anguloY = hub.imu.tilt()
    luz_esquerda = sensor_esquerdo.reflection()
    luz_direita = sensor_direito.reflection()

    erro = luz_esquerda - luz_direita

    derivada = erro - erro_anterior

    taxa_curva = (erro * KP) + (derivada * KD)

    erro_anterior = erro

    
    if anguloX > 15:
        POTENCIA_BASE = 100

    elif anguloX < -5:
        POTENCIA_BASE = 40

    else:
        POTENCIA_BASE = 70

    potencia_esquerda = POTENCIA_BASE + taxa_curva
    potencia_direita = POTENCIA_BASE - taxa_curva

    potencia_esquerda = max(-100, min(100, potencia_esquerda))
    potencia_direita = max(-100, min(100, potencia_direita))

    motor_esquerdo.dc(potencia_esquerda)
    motor_direito.dc(potencia_direita)

    desvio()
    confere_prata()

def Virar(angle):
    #zera a guinada
    hub.imu.reset_heading(0)
    if angle > 0:
        while hub.imu.heading() < angle:
            motor_direito.dc(-80)
            motor_esquerdo.dc(80)
    else:
        while hub.imu.heading() > angle:
            motor_direito.dc(80)
            motor_esquerdo.dc(-80)

    motor_esquerdo.dc(0)
    motor_direito.dc(0)

def virar_esq_atepreto(angle):

    hub.imu.reset_heading(0)

    while hub.imu.heading() > angle and sensor_esquerdo.reflection() > 25:
        motor_direito.dc(80)
        motor_esquerdo.dc(-80)

    motor_esquerdo.dc(0)
    motor_direito.dc(0)

def virar_dir_atepreto(angle):
    Virar(30)

    hub.imu.reset_heading(0)

    while hub.imu.heading() < angle and sensor_direito.reflection() > 25:
        motor_direito.dc(-80)
        motor_esquerdo.dc(80)

    motor_esquerdo.dc(0)
    motor_direito.dc(0)

def confere_verde():
    if ((sensor_direito.color() == Color.GREEN) or (sensor_direito.color() == Color.CYAN)) or ((sensor_esquerdo.color() == Color.GREEN) or (sensor_esquerdo.color() == Color.CYAN)):
        motor_esquerdo.dc(0)
        motor_direito.dc(0)
        wait(500)
        robo.straight(-10)
        
        if ((sensor_direito.color() == Color.GREEN) or (sensor_direito.color() == Color.CYAN)) and ((sensor_esquerdo.color() == Color.GREEN) or (sensor_esquerdo.color() == Color.CYAN)):
            motor_esquerdo.dc(0)
            motor_direito.dc(0)
            wait(1000)

            Virar(180)
            robo.straight(50)

        elif (sensor_direito.color() == Color.GREEN) or (sensor_direito.color() == Color.CYAN):
            motor_esquerdo.dc(0)
            motor_direito.dc(0)
            wait(1000) 
            robo.straight(90)
            virar_dir_atepreto(90)
            Virar(5)

        elif (sensor_esquerdo.color() == Color.GREEN) or (sensor_esquerdo.color() == Color.CYAN):
            motor_esquerdo.dc(0)
            motor_direito.dc(0)
            wait(1000) 
            robo.straight(90)
            virar_esq_atepreto(-90)
            Virar(-5)

def rebolar_curva():
    if sensor_direito.reflection() < 20 and sensor_esquerdo.reflection() < 20:
        motor_esquerdo.dc(0)
        motor_direito.dc(0)
        wait(10)
        robo.straight(60)
        virar_esq_atepreto(-15)
        motor_esquerdo.dc(0)
        motor_direito.dc(0)
        wait(10)
        if sensor_direito.reflection() < 30:
            Virar(10)
            robo.straight(50)

        else:
            virar_dir_atepreto(95)
            motor_esquerdo.dc(0)
            motor_direito.dc(0)

            if sensor_direito.reflection() < 35:
                robo.straight(-50)

            else:
                virar_esq_atepreto(-250)
        
def desvio():
    if ultrasonicoFrente.distance() < 50:
        ultrasonicoFrente.lights.on(100)
        ultrasonicoLado.lights.on(100)
        motor_esquerdo.dc(0)
        motor_direito.dc(0)
        wait(500)
        robo.straight(-100)
        Virar(90)

        robo.straight(300)

        Virar(-90)

        while ultrasonicoLado.distance() > 250:
            motor_direito.dc(80)
            motor_esquerdo.dc(80)

        while ultrasonicoLado.distance() < 250:
            motor_direito.dc(80)
            motor_esquerdo.dc(80)

        robo.straight(150)

        Virar(-75)

        while sensor_direito.reflection() > 30:
            motor_direito.dc(80)
            motor_esquerdo.dc(80)

        robo.straight(50)
        virar_dir_atepreto(60)
        ultrasonicoFrente.lights.off()
        ultrasonicoLado.lights.off()

def confere_prata():
    mensagem = radio.observe(61)
    
    if mensagem == "PRATA":
        motor_direito.dc(0)
        motor_esquerdo.dc(0)
        robo.straight(100)
        robo.straight(-150)
    
        wait(1000)
    
    else:
        pass

while sensor_direito.color() != Color.RED or sensor_esquerdo.color() != Color.RED:

    PID()
    confere_verde()
    rebolar_curva()
    desvio()
