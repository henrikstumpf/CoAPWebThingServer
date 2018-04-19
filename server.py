from coap_debug import CoapServer, CoapResource

VALUE_TYPE_NUMBER = 'number'
VALUE_TYPE_STRING = 'string'
VALUE_TYPE_BOOLEAN = 'boolean'

VALUE_UNIT_PERCENT = 'percent'
VALUE_UNIT_CELSIUS = 'celsius'
VALUE_UNIT_LUX = 'lux'

class WebThingServer(CoapServer):
    """Server to represent a Web Thing over CoAP."""

    def __init__(self, ip, port):
        super().__init__(ip, port)
        self.things = []

    def addThing(self, thing):
        print(thing)
        print(thing.get_state())
        self.addResource(thing)
        #TODO besserer Zugriff
        for property_ in thing.properties:
            property_ = thing.properties[property_]
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
        self.href = "things/" + self.name
        super().__init__(self.href, server, self.get_state, None)

    def get_state(self):
        """
        Return the thing state as a Thing Description.

        Returns the state as a dictionary.
        """
        return {
            'name': self.name,
            'type': self.type,
            'properties': self.get_property_states(),
            'actions': {action.name: action.description for name, description in self.actions},
            'href': self.href
        }, 50

    def get_property_states(self):
        """
        Return the property states as a dictionary
        """
        property_states = {}
        #TODO besserer Zugriff
        for property_ in self.properties:
            property_ = self.properties[property_]
            property_states[property_.name] = {
                'type': property_.type,
                'unit': property_.unit,
                'description': property_.description,
                'href': property_.href
            }
        return property_states

    def addProperty(self, name, type_="boolean", unit="", description="", \
                    handle_get=None, handle_put=None):
        property_ = Property(self.server, self, name, type_, unit, description, \
                             handle_get, handle_put)
        self.properties[property_.name] = property_

    def removeProperty(self, property_):
        self.properties.pop(property_.name)
        self.server.deleteResource(property_.href)

    def addAction(self, action):
        self.actions[action.name] = action

    def removeAction(self, action):
        self.actions.pop(action.name)
        self.server.deleteResource(action.href)

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
        self.value = None
        self.type = type_
        self.unit = unit
        self.description = description
        self.href = self.thing.href + "/properties/" + self.name
        super().__init__(self.href, server, handle_get, handle_put)

class Action(CoapResource):
    """A Web Thing Action."""

    def __init__(self, server, thing, name, description):
        pass
