# -*- coding: utf-8 -*-
import xlrd
from models import Storage



class ExcelFileLoader():

    def __init__(self, filepath):
        self.filepath = filepath

    def load_data(self):
        android_store = self.process_records('android', 0)
        ios_store = self.process_records('ios', 1)
        return android_store, ios_store

    def process_records(self, os_name, sheet_num):
        store = Storage(os_name)
        input = self.parse_excel_file(self.filepath, sheet_num)
        for row in input:
            try:
                device_name = row[1]
                device_type = row[2]
                os_version = row[3]
                page_views = float(row[4])
            except Exception as e:
                print row
                print e
            store.add_record(device_name, device_type, os_version, page_views)
        print "{0} records: {1}     {2} pageviews".format(os_name, len(store.records), store.pageviews)
        return store

    def parse_excel_file(self, datafile, sheet_num):
        workbook = xlrd.open_workbook(datafile)
        sheet = workbook.sheet_by_index(sheet_num)

        num_rows = sheet.nrows
        num_col = sheet.ncols - 0
        data = [[str(sheet.cell_value(r, col)).strip().lower()
                    for col in range(num_col)]
                        for r in range(1, num_rows)]
        return data
