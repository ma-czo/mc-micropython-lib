import machine
import time
from mc_servo.pca9685 import *
'''def pwm_demo()
    from machine import Pin, PWM
    from mc_servo.pwm import ServoCtrlPWM
    servo_ctrl = ServoCtrlPWM([PWM(Pin(1)), PWM(Pin(5))])
    servo_ctrl.setup(periodUs=20000, minPulseUs=1000, maxPulseUs=2000)
    left_arm = servo_ctrl(0)
    left_arm.setAngle(-90),
'''


def pca9685_demo():
    i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4), freq=20000)

    servo_ctrl = ServoCtrlPCA9685(i2c, addr_pca9685())
    servo_ctrl.setup()
    right_arm = servo_ctrl.servo(0)
    right_arm.set_percent(0)
    time.sleep_ms(1000)
    right_arm.set_percent(50)
    time.sleep_ms(1000)
    right_arm.set_percent(100)


if __name__ == '__main__':
    pca9685_demo()
