import os
from collections import OrderedDict

import requests
import xlrd

from fin_scrapy.utils.mongohandler import *

DAMODARN_URL = "http://www.stern.nyu.edu/~adamodar/pc/datasets/betas.xls"
MONGO_ADDRESS = 'mongodb://localhost:27017/'

MONGO_CONNECTION = Mongo_Client_Wrapper(MONGO_ADDRESS)


def get_titles_row(row_values):
    is_row = False
    titles = []
    for val in row_values:
        titles.append(val)
        if "Industry Name" == val:
            is_row = True

    if is_row == False:
        titles = None
    return titles


def parse_damodarn_data_set(file_path):
    # Open the workbook and select the first worksheet
    wb = xlrd.open_workbook(file_path)
    sh = wb.sheet_by_index(0)
    # List to hold dictionaries
    industry_data = []
    keys = []
    started_row = 0
    # Iterate through each row in worksheet and fetch values into dict
    for rownum in range(1, sh.nrows):

        row_values = sh.row_values(rownum)
        titles = get_titles_row(row_values)
        if titles is not None:
            keys = titles
            started_row = rownum + 1
            break

    for rownum in range(started_row, sh.nrows):
        data = OrderedDict()
        index = 0
        row_values = sh.row_values(rownum)
        for t in keys:
            data[t] = row_values[index]
            index += 1
        industry_data.append(data)

    return industry_data


def download_damodarn_dataset():
    r = requests.get(DAMODARN_URL)
    temp_file_name = '.{}'.format(hash(os.times()))
    if r.status_code == 200:
        with open(temp_file_name, "wb") as f:
            f.write(r.content)
        data = parse_damodarn_data_set(temp_file_name)
        os.remove(temp_file_name)
        for i in data:
            MONGO_CONNECTION.mongo_insert("beta", i)
