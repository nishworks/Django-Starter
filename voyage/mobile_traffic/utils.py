# -*- coding: utf-8 -*-

import operator


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

    def sortedList(self):
        return sorted(self.storage.iteritems(),
                            key=operator.itemgetter(1), reverse=True)

class PageviewMixin(object):

    def __init__(self):
        self.phone = 0
        self.tablet = 0
        self.pageviews = 0
        self.devices = AdvancedDict()

    def get_sorted_device_stats(self):
        return self.devices.sortedList()

def process_osversion(os_version):
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


def process_query(self, query):
    """
        Input cases:
        5.x, 5.x.x, 5.1.x, x.x.x, x.x, x
        5.1.x 5.1.0, 5.1, 5
    """
    precision = 0
    x, xx, xxx = None, None, None
    if len(query) > 5:
        raise Exception
    splits = query.split('.')

    if len(splits) > 0:
        precision += 1
        if splits[0].isdigit():
            x = int(splits[0])

    if len(splits) > 1:
        precision += 1
        if splits[1].isdigit():
            x = int(splits[1])

    if len(splits) > 2:
        precision += 1
        if splits[2].isdigit():
            x = int(splits[2])
    return x, xx, xxx, precision
