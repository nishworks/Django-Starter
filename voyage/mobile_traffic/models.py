# -*- coding: utf-8 -*-

from utils import *

class Record():

    def __init__(self, os, os_version, device_type, model, model_id, pageviews):
        self.os = os
        self.os_version = os_version
        self.device_type = device_type
        self.model = model
        self.model_id = model_id
        self.pageviews = pageviews
        self.x, self.xx, self.xxx =  self.detach_os_versions(self.os_version)

    def detach_os_versions(self, os_version):
        x, xx, xxx = 0, 0, 0
        splits = str(os_version).split(".")
        sLen = len(splits)
        if sLen > 0:
            if splits[0].isdigit() and splits[0] != '0':
                x = splits[0][:1]
        if sLen > 1:
            if splits[1].isdigit() and splits[1] != '0':
                if splits[0].isdigit():
                    xx = splits[1][:1]
        if sLen > 2:
            if splits[2].isdigit() and splits[2] != '0':
                if splits[1].isdigit():
                    xxx = splits[2][:1]
        return x, xx, xxx

    def matches_x_os_version(self, x=0, xx=0, xxx=0):
        if x != 0 and x != self.x:
            return False
        if xx != 0 and self.xx != xx:
            return False
        if xxx != 0 and self.xxx != xxx:
            return False
        return True

    def matches_os_verson(self, version):
        x, xx, xxx = self.detach_os_versions(version)
        return self.matches_x_os_version(x, xx, xxx)

    def log(self):
        "{0} : {1}".format(self.model, self.pageviews)

    def get_os_version(self, precision):
        if precision == 'x':
            return self.x
        elif precision == 'xx':
            return self.x + '.' + self.xx
        elif precision =='xxx':
            return self.x + '.' + self.xx + '.' + self.xxx
        else:
            raise Exception("Record: get_os_version() method incorrectly \
            used %s is not valid precision identifier" % precision)

class Storage():

    def __init__(self, records, pageviews, devicetype_pageviews):

        self.pageviews = pageviews
        self.records = records

    def query(self, os_type, os_version, global_threshold, local_threshold):
        pass

