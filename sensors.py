from sense_hat import SenseHat
import os
import time


class Sensors:

    def __init__(self):
        self.sense = SenseHat()
        self.temps = [None] * 3

    def get_enviro_data(self):
        return self._corrected_temp(), self.sense.get_pressure(), self.sense.get_humidity()

    def _corrected_temp(self):
        t1 = self.sense.get_temperature_from_humidity()
        t2 = self.sense.get_temperature_from_pressure()
        t_cpu = self._get_cpu_temp()

        # calculates the real temperature compesating CPU heating
        t = (t1 + t2) / 2
        t_corr = t - ((t_cpu-t) / 1.5)
        t_corr = self._get_smooth(t_corr)
        return t_corr

    def _get_cpu_temp(self):
        res = os.popen("vcgencmd measure_temp").readline()
        t = float(res.replace("temp=", "").replace("'C\n", ""))
        return(t)

    # use moving average to smooth readings
    def _get_smooth(self, x):
        if self.temps[0] is None:
            self.temps = [x, x, x]
        self.temps[2] = self.temps[1]
        self.temps[1] = self.temps[0]
        self.temps[0] = x
        xs = (self.temps[0] + self.temps[1] + self.temps[2]) / 3
        return(xs)

    def draw(self, x, y, r, g, b):
        self.sense.set_pixel(x, y, r, g, b)

    def fill(self, r, g, b):
        pixels = [(r, g, b)] * 64
        #pixels = [
        #    r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,
        #    r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,
        #    r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,
        #    r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,
        #    r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,
        #    r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,
        #    r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,
        #    r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b,r,g,b
        #]
        self.sense.set_pixels(pixels)

    def clear(self):
        self.fill(0, 0, 0)
