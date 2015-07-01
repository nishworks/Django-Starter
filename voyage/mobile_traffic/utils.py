# -*- coding: utf-8 -*-

DEVICE_TYPES = {
    "phone": 1,
    "tablet": 2
}

OS_TYPES = {
    'android': 1,
    'ios': 2
}


class AdvancedDict():

    def __init__(self):
        self._storage = dict()

    def put(self, key, value):
        if key not in self._storage:
            self._storage[key] = 0
        self._storage[key] += value

    def get(self, key):
        if key in self._storage:
            return self._storage[key]
        else:
            raise Exception("Key %s not found" % key)