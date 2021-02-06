def pwm_demo()
    from machine import Pin, PWM
    from mc_servo.pwm import ServoCtrlPWM
    servo_ctrl = ServoCtrlPWM([PWM(Pin(1)), PWM(Pin(5))])
    servo_ctrl.setup(periodUs=20000, minPulseUs=1000, maxPulseUs=2000)
    left_arm = servo_ctrl(0)
    left_arm.setAngle(-90),

def pca9685_demo():
    from mc_servo.pwm import ServoCtrlPCA9685 , addr_pca9685
    I2C
    i2c = I2C(freq=400000)

    servo_ctrl = ServoCtrlPCA9685(i2c, addr_pca9685(a0=1))
    servo_ctrl.setup(periodUs=20, minPulseUs=1, maxPulseUSs=2)
    right_arm = servoctrl.servo(0)
    right_arm_servo.setPerc(50)
    servo_ctrl.servo(2).setPulseUs(1500)
    servo_ctrl.servo(3).setAngle(-15)

def main():
    pwm_demo()
    pca9685_demo()

if __name__ == "__main__":
    main()