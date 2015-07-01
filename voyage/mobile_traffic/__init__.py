# -*- coding: utf-8 -*-
from data_loader import ExcelFileLoader

_loader = ExcelFileLoader(filepath='../uploads/traffic.xlsx')


android_Store, ios_store = _loader.load_data()