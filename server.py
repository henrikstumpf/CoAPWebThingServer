from coap import CoapServer, CoapResource

class WebThingServer(CoapServer):
    """Server to represent a Web Thing over CoAP."""

    def __init__(self, ip, port, things):
        super().__init__(self, ip, port)
        self.things = things
        for thing in self.things:
            self.addThing(thing)

    def addThing(self, thing):
        self.addResource(thing)
        for property_ in thing.properties:
            self.addResource(property_)
        for action in thing.actions:
            self.addResource(action)

class Thing(CoapResource):
    """A Web Thing."""

    def __init__(self, server, name, type_='thing', description=''):
        """
        Initialize the object.

        name -- the thing's name (also used as identifier)
        type -- the thing's type
        description - description of the thing
        """
        self.name = name
        self.type = type_
        self.description = description
        self.properties = {}
        self.actions = {}
        self.href = "/things/" + self.name
        super().__init__(self, self.href, server, self.get_state, None)

    def get_state(self):
        """
        Return the thing state as a Thing Description.

        Returns the state as a dictionary.
        """
        return {
            'name': self.name,
            'type': self.type,
            'properties': self.get_property_states(),
            'actions': {action.name: action.description} for name, description in self.actions,
            'href': self.href
        }

    def get_property_states(self):
        """
        Return the property states as a dictionary
        """
        property_states = {}
        for property_ in self.properties:
            property_states[property_.name] = {
                'type': property_.type,
                'unit': property_.unit,
                'description': property_.descritpion
            }
        return property_states

    def addProperty(self, property_):
        self.properties[property_.name] = property_

    def removeProperty(self, property_):
        self.properties.pop(property_.name)
        self.server.deleteResource(property_.href)

    def addAction(self, action):
        self.actions[action.name] = action

    def removeAction(self, action):
        self.actions.pop(action.name)
        self.server.deleteResource(action.href)

class Unit(object):
    def __init__(self, unit):
        self.name = unit
        if unit = None:
            self.symbol = ''
        elif unit = 'percent':
            self.symbol = '%'
        elif unit = 'celsius':
            self.symbol = '°C'
        elif unit = 'lux':
            self.symbol = ' lux'

    def __str__(self):
        return self.symbol

class Value(object):
    """A Value that can be held by a Property"""

    def __init__(self, value, type_, unit=None):
        """
        Initialize the object.

        value -- the value of the Value object
        type -- the value's type
        unit -- the unit of the value, if any
        """
        if type_ == VALUE_TYPE_NUMBER:
            self.value = float(value)
        elif type_ == VALUE_TYPE_STRING:
            self.value = str(value)
        elif type_ == VALUE_TYPE_BOOLEAN:
            self.value = bool(value)
        else:
            #TypeError

        self.type = type_
        self.unit = unit

    def get(self):
        return self.value

    def __str__(self):
        return str(self.value) + str(self.unit)

class Property(CoapResource):
    """A Web Thing Property."""

    def __init__(self, server, thing, name, type_="boolean", unit="", description="", handle_get=None, handle_put=None):
        """
        Initialize the object.

        thing -- the Thing this property belongs to
        name -- name of the property
        value -- value object to hold the property value
        description -- a description of the property
        """
        self.thing = thing
        self.name = name
        self.value = value
        self.description = description
        self.href = self.thing.href + "/properties/" + self.name
        super().__init__(self, self.href, server, handle_get, handle_put)

class Action(CoapResource):
    """A Web Thing Action."""

    def __init__(self, server, thing, name, description):
        pass
