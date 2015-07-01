# -*- coding: utf-8 -*-

from utils import *

class Stat():

    def __init__(self, version):
        self.version = version
        self.pageviews = 0
        self.devices_pageviews = AdvancedDict()


class StatsDict():

    def __init__(self):
        self._os_storage = dict()
        self._os_pageviews = AdvancedDict()

    def put_record(self, key, record):
        if key not in self._os_storage:
            self._os_storage[key] = Stat()
        self._os_pageviews.put(key, record.pageviews)
        self._os_storage[key].pageviews += record.pageviews
        self._os_storage[key].devices_pageviews.put(record.model, record.pageviews)

    def get_stats(self, version):
        pass




class StatStorage():

    def __init__(self):
        self.deviceType_pageviews = AdvancedDict()
        self.x = AdvancedDict()
        self.xx = AdvancedDict()
        self.xxx = AdvancedDict()

    def construct_stats(self, records):

        for r in records:
            #deviceType pageviews
            self.put_pageviews_deviceType(r)
            self.put_xVersion_pageviews(r)


    def put_pageviews_deviceType(self, record):
        if record.device_type == DEVICE_TYPES['phone']:
            self.deviceType_pageviews.put('phone', record.pageviews)
        else:
            self.deviceType_pageviews.put('tablet', record.pageviews)

    def put_xVersion_pageviews(self, record):
        version = record.get_os_version('x')
        self.x.put(version, record.pageviews)

    def put_xxVersion_pageviews(self, record):
        version = record.get_os_version('xx')
        self.xx.put(version, record.pageviews)

    def put_xxxVersion_pageviews(self, record):
        version = record.get_os_version('xxx')
        self.xxx.put(version, record.pageviews)





