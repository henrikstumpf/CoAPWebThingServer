from ds18x20 import DS18X20
from machine import I2C
from machine import PWM
from machine import unique_id
from micropython import const
from os import urandom
from onewire import OneWire
from ubinascii import hexlify

from dht import DHT22 as DHT
from machine import Pin as GPIO

I2C_SCL = const(5)
I2C_SDA = const(4)
I2CFREQ = const(100000)
ONEWIRE = const(12)

I2CBus = I2C(scl=GPIO(I2C_SCL), sda=GPIO(I2C_SDA), freq=I2CFREQ)
OneWireBus = OneWire(GPIO(ONEWIRE))
DS18B20Bus = DS18X20(OneWireBus)

mac = int.from_bytes(unique_id(), 'big')
def uid():
    return int.from_bytes(urandom(8), 'big')

#esp8266 nodemcu specific definitions
pwm_pins = [0, 2, 4, 5, 12, 13, 14, 15]

class DS18B20(TemperatureSensor):
    def __init__(self, server, addr):
        self.rom_id = addr
        super().__init__(server, 'ds18b20-' + str(uid), self.read)

    def read(self):
        return self._get_value(), 0

    def _get_value(self):
        DS18B20Bus.convert_temp()
        time.sleep_ms(750)
        temp = DS18B20Bus.read_temp(self.rom_id)
        return temp

class DHT22Temp(TemperatureSensor, DHT):
    def __init__(self, server, pin):
        MultiLevelSensor.__init__(self, server, 'dht22-' + str(uid), self.read)
        DHT.__init__(self, GPIO(pin))

    def read(self):
        return self._get_value(), 0

    def _get_value(self):
        self.measure()
        temp = self.temperature()
        return temp

class DHT22Temp(MultiLevelSensor, DHT):
    def __init__(self, server, pin):
        MultiLevelSensor.__init__(self, server, 'dht22-' + str(uid), self.read)
        DHT.__init__(self, GPIO(pin))

    def read(self):
        return self._get_value(), 0

    def _get_value(self):
        self.measure()
        hum = self.humidity()
        return hum

class GPIOLight(OnOffLight):
    def __init__(self, server, pin):
        self._pin = GPIO(pin, GPIO.OUT)
        super().__init__(server, 'light-' + str(uid), \
                         self.get_state, self.set_state)

    def get_state(self):
        return self._pin.value(), 0

    def set_state(self, state):
        if state == 'on' or state == '1' or state == 'True':
            self._pin.on()
            return True, 0
        else:
            self._pin.off()
            return False, 0

class PWMLight(DimmableLight):
    def __init__(self, server, pin, freq=1000):
        super().__init__(server, 'light-' + str(uid), \
                         self.get_state, self.set_state, \
                         self.get_level, self.set_level)
        if pin in pwm_pins:
            self.dimmable = True
            self._pin = PWM(GPIO(pin), freq=freq, duty=0)
        else:
            self.dimmable = False

    def get_state(self):
        return self._pin.value(), 0

    def set_state(self, state):
        if state == 'on' or state == '1' or state == 'True':
            self._pin.on()
            return True, 0
        else:
            self._pin.off()
            return False, 0

    def get_level(self):
        return self._pin.duty(), 0

    def set_level(self, level):
        #convert brightness from percent (0 - 100) to duty (0 - 1023)
        duty = round(1023 * (int(brightness)/100))
        self._pin.duty(duty)
        return level, 0

class RGBLight(OnOffColorLight):
    def __init__(self, server, pin_red, pin_green, pin_blue, freq=1000):
        super().__init__(server, 'light-' + str(uid), \
                         self.get_state, self.set_state, \
                         self.get_color, self.set_color)
        self._pin_r = PWM(GPIO(pin_red), freq=freq, duty=0)
        self._pin_g = PWM(GPIO(pin_green), freq=freq, duty=0)
        self._pin_b = PWM(GPIO(pin_blue), freq=freq, duty=0)

    def get_state(self):
        if self._pin_r.value() | self._pin_g.value() | self._pin_b.value():
            return True, 0
        else:
            return False, 0

    def set_state(self, state):
        if state == 'on' or state == '1' or state == 'True':
            self._pin_r.on()
            self._pin_g.on()
            self._pin_b.on()
            return True, 0
        else:
            self._pin_r.off()
            self._pin_g.off()
            self._pin_b.off()
            return False, 0

    def get_color(self):
        red = round((self._pin_r.duty() / 1023) * 255)
        green = round((self._pin_g.duty() / 1023) * 255)
        blue = round((self._pin_b.duty() / 1023) * 255)
        hex_color = (red << 16) | (green << 8) | blue
        return hex(hex_color), 0

    def set_color(self, color):
        #color must be in hex format (e.g. 'ff26e9')
        hex_color = int(color, 16)
        red = ((hex_color & 0xff0000) >> 16) / 255
        green = ((hex_color & 0x00ff00) >> 8) / 255
        blue = ((hex_color & 0x0000ff) / 255

        self._pin_r.duty(round(1023 * (red/100)))
        self._pin_g.duty(round(1023 * (green/100)))
        self._pin_b.duty(round(1023 * (blue/100)))

        return color, 0
