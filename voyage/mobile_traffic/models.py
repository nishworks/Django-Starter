# -*- coding: utf-8 -*-
from utils import *

class Record(PageviewMixin):

    def __init__(self, x, xx, xxx):
        # init pageviewmixin
        self.x, self.xx, self.xxx = x, xx, xxx

    def put_stat(self, device_name, device_type, pageviews):
        self.pageviews += pageviews
        if device_type == 'tablet':
            self.tablet += pageviews
        else:
            self.phone += pageviews
        self.devices.put(device_name, pageviews)

    def match(self, x=None, xx=None, xxx=None):
        if x is not None and x != self.x:
            return False
        if xx is not None and self.xx != xx:
            return False
        if xxx is not None and self.xxx != xxx:
            return False
        return True

    def osversion(self, precision=3):
        if precision == 1:
            return str(self.x) + 'x.x'
        elif precision == 2:
            return str(self.x) + '.' + str(self.xx) + '.x'
        elif precision == 3:
            return str(self.x) + '.' + str(self.xx) + '.' + str(self.xxx)
        else:
            raise Exception("Record: get_os_version() method incorrectly \
            used %s is not valid precision identifier" % precision)

class ResultStat(PageviewMixin):

    def __init__(self, version):
        # init pageviewmixin
        self.version = version

    def merge_record(self, record):
        for d in record.devices:
            views = record.devices[d]
            self.devices.put(d, views)
        self.pageviews += record.pageviews
        self.tablet += record.tablet
        self.phone += record.phone

class ResultSet():

    def __init__(self, precision):
        self.stats = dict()
        self.precision = precision

    def process_record(self, record):
        os_version = record.osversion(self.precision)
        if os_version not in self.stats:
            self.stats[os_version] = Stat(os_version)
        self.stats[os_version].merge_record(record)

class RecordStore(PageviewMixin):

    def __init__(self, name):
        # init pageviewmixin
        self.name = name
        self.records = dict()
        self.tablet_devices = set()
        self.phone_devices = set()

    def add_record(self, device_name, device_type, osversion, pageviews):
        self.pageviews += pageviews
        x, xx, xxx, version = process_osversion(osversion)
        if device_type == 'tablet':
            self.tablet += pageviews
            self.tablet_devices.add(device_name)
        else:
            self.phone += pageviews
            self.phone_devices.add(device_name)
        if version not in self.records:
            self.records[version] = Record(x, xx, xxx)
        self.devices.put(device_name, pageviews)
        self.records[version].put_stat(device_name, device_type, pageviews)

    def query(self, query):
        x, xx, xxx, precision = process_query(query)
        result_set = ResultSet(precision)
        for record in self.records:
            if not record.match(x, xx, xxx):
                continue
            result_set.process_record(record)
        return result_set

    def build_global_stats(self):
        self.sorted_devices = sorted(self.devices.storage.iteritems(),
                            key=operator.itemgetter(1), reverse=True)
        self.xxx = None
        self.xx = None
        self.x = None
