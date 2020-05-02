import globals.globals as globals
import logging

class Setting():

    def __init__(self, value):
        self.value = value

    def get(self):
        return self._value

    def set(self, target):
        logging.debug(f"Setting changed to {target}, redrawing ui's")
        self._value = target
        globals.events.setting_change()

    value = property(get, set)
