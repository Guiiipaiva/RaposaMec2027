from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait

motor_esquerdo = Motor(Port.A)
motor_direito = Motor(Port.B)

motor_esquerdo.run(400)
motor_direito.run(-400)

wait(200) 

LIMITE_TORQUE = 200 

while True:
    forca_esq = abs(motor_esquerdo.load())
    forca_dir = abs(motor_direito.load())
    print(forca_dir)
    if forca_esq > LIMITE_TORQUE or forca_dir > LIMITE_TORQUE:
        break
        
    wait(10)

motor_esquerdo.stop()
motor_direito.stop()
