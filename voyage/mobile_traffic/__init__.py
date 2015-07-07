# -*- coding: utf-8 -*-
from data_loader import ExcelFileLoader

_loader = ExcelFileLoader(filepath='../uploads/traffic.xlsx')


android_store, ios_store = _loader.load_data()

android_store.process_stats()
