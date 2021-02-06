from machine import PWM

class ServoPWM(Servo):
    def __init__(self, pwms):
        self.pwms = pwms
