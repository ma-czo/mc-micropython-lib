from machine import I2C


def pca9685_addr(a5=0, a4=0, a3=0, a2=0, a1=0, a0=0) -> int:
    return 0x40 + \
           (a5 << 5) + \
           (a4 << 4) + \
           (a3 << 3) + \
           (a2 << 2) + \
           (a1 << 1) + \
           a0


class PCA9685ServoCtrl(object):
    _REG_ADDR_MODE1: int = 0x00
    _REG_ADDR_LED0_OFF_L: int = 0x08
    _REG_ADDR_LED1_OFF_L: int = 0x0C
    _REG_ADDR_PRE_SCALE: int = 0xFE
    _REG_LED_ADDR_SIZE: int = _REG_ADDR_LED1_OFF_L - _REG_ADDR_LED0_OFF_L
    _MODE1_RESET: int = 1 << 7
    _MODE1_AI: int = 1 << 5
    _MODE1_SLEEP: int = 1 << 4

    def __init__(self, i2c: I2C, addr: int):
        self._addr: int = addr
        self._i2c = i2c
        self._clock_hz: int = 25000000
        self._pwm_count_max: int = 4096
        self._period_us: int = 20000
        self.min_pulse_us: int = 1000
        self.max_pulse_us: int = 2000

    def _pre_scale(self) -> int:
        return int((self._clock_hz * self._period_us / (1e6 * self._pwm_count_max)) - 1)

    def setup(self, period_us: int = 20000, min_pulse_us: int = 1000, max_pulse_us: int = 2000):

        self._period_us = period_us
        self.min_pulse_us = min_pulse_us
        self.max_pulse_us = max_pulse_us
        if self._addr in self._i2c.scan():
            print("Device I2C addr:", self._addr, " is detected, clock pre_scale: ", self._pre_scale())
        else:
            print("Device I2C addr:", self._addr, " not detected")

        self._i2c.writeto_mem(self._addr, self._REG_ADDR_MODE1,
                              (self._MODE1_AI + self._MODE1_SLEEP).to_bytes(1, 'little'))
        self._i2c.writeto_mem(self._addr, self._REG_ADDR_PRE_SCALE,
                              self._pre_scale().to_bytes(1, 'little'))
        self._i2c.writeto_mem(self._addr, self._REG_ADDR_MODE1,
                              (self._MODE1_AI + self._MODE1_RESET).to_bytes(1, 'little'))

    def channel(self, channel_id):
        return PCA9685Channel(self, channel_id)

    def duration_to_pwm_value(self, duration_us: int) -> int:
        duration_us = min(duration_us, self.max_pulse_us)
        duration_us = max(duration_us, self.min_pulse_us)
        return int(self._pwm_count_max * duration_us / self._period_us)

    def set_pwm_value(self, channel: int, value: int):
        if channel < 0 or channel > 15:
            raise IndexError("Requested channel ", channel, " but only values from range  0..15 are allowed.")
        channel_addr = self._REG_ADDR_LED0_OFF_L + channel * self._REG_LED_ADDR_SIZE
        self._i2c.writeto_mem(self._addr, channel_addr, int(value).to_bytes(2, 'little'))


class PCA9685Channel(object):

    def __init__(self, ctrl: PCA9685ServoCtrl, channel: int):
        if channel < 0 or channel > 15:
            raise IndexError("Requested channel ", channel, " but only values from range  0..15 are allowed.")
        self._ctrl = ctrl
        self._channel = channel

    def set_pulse_us(self, duration_us: int):
        self._ctrl.set_pwm_value(self._channel, self._ctrl.duration_to_pwm_value(duration_us))

    def set_percent(self, percent: float):
        duration = self._ctrl.min_pulse_us + percent / 100 * (self._ctrl.max_pulse_us - self._ctrl.min_pulse_us)
        self.set_pulse_us(int(duration))

    def set_angle(self, angle: float):
        self.set_percent((angle + 90) / 180 * 100)
