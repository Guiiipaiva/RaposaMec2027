from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction, Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from pybricks.messaging import BLERadio

#Inicializa o Hub
hub = PrimeHub()
radio = BLERadio(observe_channels=[61])

#Configura os Motores da Esteira
motor_esquerdo = Motor(Port.A, Direction.COUNTERCLOCKWISE)
motor_direito = Motor(Port.B, Direction.CLOCKWISE)

#salva as inclinações do robo 
anguloX, anguloY = hub.imu.tilt()

#Configura a DriveBase
robo = DriveBase(motor_esquerdo, motor_direito, wheel_diameter=45, axle_track=112)

#Configura os Sensores nas suas portas
sensor_esquerdo = ColorSensor(Port.C)
sensor_direito = ColorSensor(Port.D)
ultrasonicoFrente = UltrasonicSensor(Port.F)
ultrasonicoLado = UltrasonicSensor(Port.E)

#desliga as luzes do sensores ultrasonicos
ultrasonicoFrente.lights.off()
ultrasonicoLado.lights.off()

#variaveis globais 
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
        POTENCIA_BASE = 30

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

    parar_motores()

def virar_esq_atepreto(angle):

    hub.imu.reset_heading(0)

    while hub.imu.heading() > angle and sensor_esquerdo.reflection() > 25:
        motor_direito.dc(80)
        motor_esquerdo.dc(-80)

    parar_motores()

def virar_dir_atepreto(angle):
    Virar(30)

    hub.imu.reset_heading(0)

    while hub.imu.heading() < angle and sensor_direito.reflection() > 25:
        motor_direito.dc(-80)
        motor_esquerdo.dc(80)

    parar_motores()

def parar_motores():
    motor_esquerdo.dc(0)
    motor_direito.dc(0)

def confere_verde():
    cores_alvo = (Color.GREEN, Color.CYAN)
    cor_dir = sensor_direito.color()
    cor_esq = sensor_esquerdo.color()

    if cor_dir in cores_alvo or cor_esq in cores_alvo:
        parar_motores()
        wait(500)
        robo.straight(-10)
        
        # Lê novamente após ir para trás
        cor_dir = sensor_direito.color()
        cor_esq = sensor_esquerdo.color()
        
        if cor_dir in cores_alvo and cor_esq in cores_alvo:
            parar_motores()
            wait(1000)
            Virar(180)
            robo.straight(50)

        elif cor_dir in cores_alvo:
            parar_motores()
            wait(1000) 
            robo.straight(90)
            virar_dir_atepreto(90)
            Virar(5)

        elif cor_esq in cores_alvo:
            parar_motores()
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
        parar_motores()
        wait(10)
        if sensor_direito.reflection() < 30:
            Virar(10)
            robo.straight(50)

        else:
            virar_dir_atepreto(95)
            parar_motores()

            if sensor_direito.reflection() < 35:
                robo.straight(-50)

            else:
                virar_esq_atepreto(-250)
        
def desvio():
    if ultrasonicoFrente.distance() < 50:
        ultrasonicoFrente.lights.on(100)
        ultrasonicoLado.lights.on(100)
        parar_motores()
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

def andar_ate_bater():
    motor_esquerdo.run(400)
    motor_direito.run(400)

    wait(250) 
    LIMITE_TORQUE = 200
    
    while True:
        forca_esq = abs(motor_esquerdo.load())
        forca_dir = abs(motor_direito.load())
        
        if forca_esq > LIMITE_TORQUE or forca_dir > LIMITE_TORQUE or ultrasonicoLado.distance() >= 350 or sensor_direito.reflection() < 25 or sensor_esquerdo.reflection() < 25:
            parar_motores()
            if ultrasonicoLado.distance() >= 350:
                opcao =  "Lado"

            elif sensor_direito.reflection() < 25 or sensor_esquerdo.reflection() < 25:
                opcao = "preto"

            else:
                opcao = "forcou"

def re_ate_bater():
    motor_esquerdo.run(-400)
    motor_direito.run(-400)

    wait(200) 

    LIMITE_TORQUE = 250

    while True:
        forca_esq = abs(motor_esquerdo.load())
        forca_dir = abs(motor_direito.load())
        if forca_esq > LIMITE_TORQUE or forca_dir > LIMITE_TORQUE:
            break
            
        wait(10)

    parar_motores()

def confere_prata():
    mensagem = radio.observe(61)
    
    if mensagem == "PRATA":
        parar_motores()
        
        wait(1000)

        area_resgate()
    
    else:
        pass

def pid_andar_reto(dis):
    rot_nec = dis / (3.14 * 45)
    rot_ini = motor_direito.angle() / 360
    rot_des = rot_ini + rot_nec
    hub.imu.reset_heading(0)
    while motor_direito.angle() / 360 <= rot_des:
        a = 0 - hub.imu.heading() * 2 
        robo.drive(POTENCIA_BASE * 2, a)
    robo.stop()

def area_resgate():
    robo.straight(200)
    if ultrasonicoLado.distance() < 200: 
        pid_andar_reto(275)
        parar_motores()
        wait(5000)
        Virar(90)
        wait(500)
        pid_andar_reto(200) 
    
    else: 
        pid_andar_reto(275)
        parar_motores()
        wait(50)
        Virar(-85)
        wait(500)
        pid_andar_reto(200) 

area_resgate()