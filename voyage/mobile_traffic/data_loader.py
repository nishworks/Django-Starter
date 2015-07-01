# -*- coding: utf-8 -*-
import xlrd
from models import Record, Storage
from utils import DEVICE_TYPES, OS_TYPES


class ExcelFileLoader():

    def __init__(self, filepath):
        self.filepath = filepath

    def load_data(self):
        android_store = self.return_os_records('android', 0)
        ios_store = self.return_os_records('ios', 1)
        return android_store, ios_store

    def return_os_records(self, os_name, sheet_num):
        records = []
        total_page_views = 0
        phone_pageviews = 0
        tablet_pageviews = 0
        input = self.parse_excel_file(self.filepath, sheet_num)
        for row in input:
            record = self.create_record(row, os_name)
            if record is not None:
                records.append(record)
                total_page_views += record.pageviews
                if row[2] == 'tablet':
                    tablet_pageviews += record.pageviews
                else:
                    phone_pageviews += record.pageviews
        print "{0} records: {1}     {2} pageviews".format(os_name, len(records), total_page_views)
        return Storage(records, total_page_views)

    def create_record(self, row, os_name):
        record = None
        try:
            model_id = row[0]
            model = row[1]
            device_type = DEVICE_TYPES[row[2]]
            os_version = row[3]
            page_views = float(row[4])
            os = OS_TYPES[os_name]
            record = Record(os, os_version, device_type, model, model_id, page_views)
        except Exception as e:
            print row
            print e
        return record

    def parse_excel_file(self, datafile, sheet_num):
        workbook = xlrd.open_workbook(datafile)
        sheet = workbook.sheet_by_index(sheet_num)

        num_rows = sheet.nrows
        num_col = sheet.ncols - 0
        data = [[str(sheet.cell_value(r, col)).strip().lower()
                    for col in range(num_col)]
                        for r in range(1, num_rows)]
        return data
