class OnOffSwitch(Thing):
    """
    On/Off Switch is a generic device type for actuators with a boolean on/off state.
    This may be used for smart plugs and light switches for example.
    """

    def __init__(self, server, name, get_state, set_state):
        super().__init__(server, name, 'onOffSwitch', 'An on/off switch')
        self.addProperty('on', 'boolean', '', 'the state of this switch', \
                        get_state, set_state)

class MultiLevelSwitch(Thing):
    """
    A switch with multiple levels such as a dimmer switch.
    """

    def __init__(self, server, name, get_state, set_state, get_level, set_level):
        super().__init__(server, name, 'multiLevelSwitch', 'A multi level switch')
        self.addProperty('on', 'boolean', '', 'the state of this switch', \
                        get_state, set_state)
        self.addProperty('level', 'number', 'percent', 'the level of this switch', \
                        get_level, set_level)

class BinarySensor(Thing):
    """
    Binary Sensor is a generic device type for sensors with a boolean on/off state.
    This may be used for smart door, infrared movement or flood sensors for example.
    """

    def __init__(self, server, name, read_sensor):
        super().__init__(server, name, 'binarySensor', 'A binary sensor')
        self.addProperty('value', 'boolean', '', 'the value of this sensor', \
                        read_sensor)

class MultiLevelSensor(Thing):
    """
    A generic multi level sensor with a value which can be expressed as a percentage.
    """

    def __init__(self, server, name, read_sensor):
        super().__init__(server, name, 'multiLevelSensor', 'A multi level sensor')
        self.addProperty('value', 'number', 'percent', 'the value of this sensor', \
                        read_sensor)

class TemperatureSensor(Thing):
    """
    A temperature sensor.
    """

    def __init__(self, server, name, read_sensor):
        super().__init__(server, name, 'thing', 'A temperature sensor')
        self.addProperty('value', 'number', 'celsius', 'the value of this sensor', \
                        read_sensor)

class OnOffLight(Thing):
    """
    A light that can be turned on and off like an LED or a bulb.
    """

    def __init__(self, server, name, get_state, set_state):
        super().__init__(server, name, 'onOffLight', 'An on/off light')
        self.addProperty('on', 'boolean', '', 'the state of this light', \
                        get_state, set_state)

class dimmableLight(Thing):
    """
    A light that can have its brightness level set.
    """

    def __init__(self, server, name, get_state, set_state, get_level, set_level):
        super().__init__(server, name, 'dimmableLight', 'A dimmable light')
        self.addProperty('on', 'boolean', '', 'the state of this light', \
                        get_state, set_state)
        self.addProperty('level', 'number', 'percent', 'the brightness level of this light', \
                         get_level, set_level)

class OnOffColorLight(Thing):
    """
    A colored light that can be switched on and off.
    """

    def __init__(self, server, name, get_state, set_state, get_color, set_color):
        super().__init__(server, name, 'onOffColorLight', 'An on/off color light')
        self.addProperty('on', 'boolean', '', 'the state of this light', \
                        get_state, set_state)
        self.addProperty('color', 'number', '', 'the color of this light', \
                         get_color, set_color)

class DimmableColorLight(Thing):
    """
    A colored light that can have its brightness level set.
    """

    def __init__(self, server, name, get_state, set_state, get_level, set_level, \
                 get_color, set_color):
        super().__init__(server, name, 'dimmableColorLight', 'A dimmable color light')
        self.addProperty('on', 'boolean', '', 'the state of this light', \
                        get_state, set_state)
        self.addProperty('level', 'number', 'percent', 'the brightness level of this light', \
                         get_level, set_level)
        self.addProperty('color', 'number', '', 'the color of this light', \
                         get_color, set_color)
