# -*- coding: utf-8 -*-

import operator
from utils import *



class Record():

    def __init__(self, x, xx, xxx):
        self.tablet = 0
        self.phone = 0
        self.pageviews = 0
        self.x, self.xx, self.xxx = x, xx, xxx
        self.stats = AdvancedDict()

    def put_stat(self, device_name, device_type, pageviews):
        self.pageviews += pageviews
        if device_type == 'tablet':
            self.tablet += pageviews
        else:
            self.phone += pageviews
        self.stats.put(device_name, pageviews)

    def query(self, x=None, xx=None, xxx=None):
        if x is not None and x != self.x:
            return False
        if xx is not None and self.xx != xx:
            return False
        if xxx is not None and self.xxx != xxx:
            return False
        return True

    def get_views(self, x, xx, xxx):
        if self.query(x,xx,xxx):
            return self.pageviews
        return 0

    def osversion(self, precision=3):
        if precision == 1:
            return str(self.x)
        elif precision == 2:
            return str(self.x) + '.' + str(self.xx)
        elif precision == 3:
            return str(self.x) + '.' + str(self.xx) + '.' + str(self.xxx)
        else:
            raise Exception("Record: get_os_version() method incorrectly \
            used %s is not valid precision identifier" % precision)

    def process_stats(self):
        self.sorted_stats = sorted(self.stats.storage.iteritems(),
                            key=operator.itemgetter(1), reverse=True)


class Storage():

    def __init__(self, name):
        self.name = name
        self.pageviews = 0
        self.phone = 0
        self.tablet = 0
        self.records = dict()
        self.devices = AdvancedDict()
        self.devicetype = dict()

    def add_record(self, device_name, device_type, os_version, pageviews):
        self.pageviews += pageviews
        x, xx, xxx, version = detach_os_versions(os_version)
        if device_type == 'tablet':
            self.tablet += pageviews
            self.devicetype[device_name] = 1
        else:
            self.phone += pageviews
            self.devicetype[device_name] = 0
        if os_version not in self.records:
            self.records[version] = Record(x, xx, xxx)
        self.devices.put(device_name, pageviews)
        self.records[version].put_stat(device_name, device_type, pageviews)

    def process_stats(self):
        for r in self.records:
            self.records[r].process_stats()
        sorted_devices = sorted(self.devices.storage.iteritems(),
                            key=operator.itemgetter(1), reverse=True)
        sorted_records = sorted(self.records.values(),
                            key=lambda record: record.pageviews, reverse=True)
        self.devices = sorted_devices
        self.records = sorted_records
        """
        for d in self.sorted_devices:
            print " {0}  :   {1}".format(d[0], d[1])
        for r in self.sorted_records:
            print " {0}  :   {1}".format(r.osversion(), r.pageviews)

        rr = self.records.get('4.4.2')
        for s in rr.sorted_stats:
            print " {0}  :   {1}".format(s[0], s[1])
        """