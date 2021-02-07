import machine
import utime
from mc_servo.pca9685 import *


def pca9685_demo():
    i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4), freq=20000)

    servo_ctrl = PCA9685ServoCtrl(i2c, pca9685_addr())
    servo_ctrl.setup()
    right_arm = servo_ctrl.channel(0)
    right_arm.set_percent(0)
    utime.sleep_ms(1000)
    right_arm.set_percent(50)
    utime.sleep_ms(1000)
    right_arm.set_percent(100)


if __name__ == '__main__':
    pca9685_demo()
