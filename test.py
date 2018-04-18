import sys
sys.path.append('C:/users/henrik/github/COAPython')
sys.path.append('C:/users/henrik/github/CoAPWebThingServer')

import random
random.seed()

from server import *

light = False
level = 0

def get_random_number():
    return random.randint(20, 30), 0

def get_light():
    return light, 0

def set_light(state):
    if bool(state):
        light = True
        print('Licht an')
    else:
        light = False
        print('Licht aus')
    return light, 0

def get_level():
    return level, 0

def set_level(level):
    level = int(level)
    print('New light level: ', level)
    return level, 0

webthing_server = WebThingServer('192.168.71.34', 5684)

sensor1 = Thing(webthing_server, 'Sensor1', description="temperature sensor")
sensor1.addProperty('temp', 'number', 'celsius', 'temperature in degress celsius', \
                    get_random_number)

sensor2 = Thing(webthing_server, 'Sensor2', description="temperature sensor")
sensor2.addProperty('temp', 'number', 'celsius', 'temperature in degress celsius', \
                    get_random_number)

sensor3 =  Thing(webthing_server, 'Sensor3', description="temperature sensor")
sensor3.addProperty('hum', 'number', 'percent', 'relative humidity in percent', \
                    get_random_number)

dimmable_light =  Thing(webthing_server, 'Licht', description="dimmable light")
dimmable_light.addProperty('state', 'boolean', '', 'wether the light is on', \
                    get_light, set_light)
dimmable_light.addProperty('level', 'number', '', 'the brightness level of the light', \
                           get_level, set_level)

webthing_server.addThing(sensor1)
webthing_server.addThing(sensor2)
webthing_server.addThing(sensor3)
webthing_server.addThing(dimmable_light)

webthing_server.start()

