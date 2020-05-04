import globals.globals as globals

class Stat():

    def __init__(self, value=0):
        self.value = value

    def get(self):
        return self._value

    def set(self, target):
        self._value = target
        globals.events.data_changed()

    value = property(get, set)

class Achievement():

    def __init__(self, value=False):
        self.value = value

    def get(self):
        return self._value

    def set(self, target):
        self._value = target
        globals.events.data_changed()

    value = property(get, set)
