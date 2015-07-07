# -*- coding: utf-8 -*-

class AdvancedDict():

    def __init__(self):
        self.storage = dict()

    def put(self, key, value):
        if key not in self.storage:
            self.storage[key] = 0
        self.storage[key] += value

    def get(self, key):
        if key in self.storage:
            return self.storage[key]
        else:
            raise Exception("Key %s not found" % key)

def detach_os_versions(os_version):
    x, xx, xxx = 0, 0, 0
    splits = str(os_version).split(".")
    sLen = len(splits)
    if sLen > 0:
        if splits[0].isdigit():
            x = int(splits[0][:1])
    if sLen > 1:
        if splits[1].isdigit():
            if splits[0].isdigit():
                xx = int(splits[1][:1])
    if sLen > 2:
        if splits[2].isdigit():
            if splits[1].isdigit():
                xxx = int(splits[2][:1])
    return x, xx, xxx, str(x)+'.'+str(xx)+'.'+str(xxx)
