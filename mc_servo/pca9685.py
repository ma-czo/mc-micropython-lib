from machine import I2C


def addr_pca9685(a5=0, a4=0, a3=0, a2=0, a1=0, a0=0):
    return 0x40 + \
           (a5 << 5) + \
           (a4 << 4) + \
           (a3 << 3) + \
           (a2 << 2) + \
           (a1 << 1) + \
           a0


class ServoCtrlPCA9685(object):

    def __init__(self, i2c: I2C, addr: int):
        self._addr: int = addr
        self._i2c = i2c
        self._clock_hz: int = 25000000
        self._count_max: int = 4096
        self._period_us: int = 20000
        self._min_pulse_us: int = 1000
        self._max_pulse_us: int = 2000

    def _prescaler(self) -> int:
        return int((self._clock_hz * self._period_us / (1e6 * self._count_max)) - 1)

    def setup(self, period_us=2000, min_pulse_us=1000, max_pulse_us=2000):
        self._period_us = period_us
        self._min_pulse_us = min_pulse_us
        self._max_pulse_us = max_pulse_us
        self._i2c.writeto_mem(self._addr, 0, b'\x00')
        if self._addr in self._i2c.scan():
            print("Device I2C ", self._addr, " is detected, prescaler ", self._prescaler())
        else:
            print("Device I2C ", self._addr, " not detected")
        self._i2c.writeto_mem(self._addr, 0, b'\x10')
        self._i2c.writeto_mem(self._addr, 0xFE, self._prescaler().to_bytes(1, 'little'))
        self._i2c.writeto_mem(self._addr, 0, b'\xA1')

    def servo(self, index):
        return ServoPCA9685(self, index)

    def duration2count(self, duration_us: int) -> int:
        duration_us = min(duration_us, self._max_pulse_us)
        duration_us = max(duration_us, self._min_pulse_us)
        return int(self._count_max * duration_us / self._period_us)

    def set_value(self, index: int, value: int):
        self._i2c.writeto_mem(self._addr, index * 4 + 8, int(value).to_bytes(2, 'little'))


class ServoPCA9685(object):

    def __init__(self, ctrl: ServoCtrlPCA9685, index: int):
        self._ctrl = ctrl
        self._index = index

    def set_pulse_us(self, duration_us: int):
        self._ctrl.set_value(self._index, self._ctrl.duration2count(duration_us))

    def set_percent(self, percent: float):
        duration = self._ctrl._min_pulse_us + percent / 100 * (self._ctrl._max_pulse_us - self._ctrl._min_pulse_us)
        self.set_pulse_us(int(duration))

    def set_angle(self, angle: float):
        self.set_percent((angle + 90) / 180 * 100)
