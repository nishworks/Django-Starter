from utils import *

class Result(PageviewMixin):

    def __init__(self, version):
        self.version = version

    def put_record(self, record):
        for d in record.devices:
            views = record.devices[d]
            self.devices.put(d, views)
        self.pageviews += record.pageviews
        self.tablet += record.tablet
        self.phone += record.phone
