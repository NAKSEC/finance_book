#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import camelot
# from camelot.core import TableList
# from camelot.parsers import Lattice, Stream
# from camelot.ext.ghostscript import Ghostscript
import json
import re

ANNOTATION = [u'\u05e8\u05d5\u05d0\u05d1', u'\u05e8\u05d5\u05d0\u05d9\u05d1']
TITLE = u'\u05e9\u05d7"  \u05d9\u05e4\u05dc\u05d0\u05d1'


def main():
    # tables = camelot.read_pdf('KPMG3.pdf', pages='58', flavor='stream')
    # print tables
    # tables.export("json", f='json')

    json_file = open("/Users/galnakash/PycharmProjects/http_poc/fin_scrapy/maya/json-page-58-table-1", "r")
    json_file = open("/Users/galnakash/PycharmProjects/http_poc/fin_scrapy/maya/json-page-60-table-1", "r")
    json_file = open("/Users/galnakash/PycharmProjects/http_poc/fin_scrapy/maya/json-page-399-table-1", "r")
    json_file = open("/Users/galnakash/PycharmProjects/http_poc/fin_scrapy/maya/json-page-84-table-1", "r")
    data = json.load(json_file, encoding='utf8')
    json_file.close()
    s = json.dumps(data).decode('unicode-escape').encode('utf8')
    print data

    context = first_order_and_label(data)
    data = context[0]
    years = context[1]

    print years
    index_of_title = None
    index_of_2017 = None
    index_of_annotation = None
    for entry in years:
        if entry['value'] == "title":
            index_of_title = entry['index']
        if entry['value'] == "2017":
            print entry
            index_of_2017 = entry['index']
        if entry['value'] == "annotation":
            index_of_annotation = entry['index']

    print index_of_title
    print index_of_2017

    f = open("log.txt", "w")

    for entry in data:
        print entry
        annotation = u"None"
        try:
            annotation = entry[index_of_annotation]
        except:
            print "error"
        try:
            number = entry[index_of_2017]
            f.write("%s ------- %s ------- annotation %s \r\n" % (entry[index_of_title].encode('utf8')[::-1],
                                                                  number.encode("utf8"),
                                                                  annotation.encode("utf8")))
        except Exception as e:
            print "error"
            print e
        for key, value in entry.items():
            regex_pattern = "^[0-9]{1,2}([,.][0-9]{1,2})?$"
            result = re.match(regex_pattern, value)
            if result:
                continue
                # print "number"
    f.close()


def first_order_and_label(data):
    escaped_data = []
    years = []
    for entry in data:
        new_entry = remove_empty_string(entry)
        escaped_data.append(new_entry)
        is_it_year_entry = False
        for key, value in new_entry.items():
            year_to_index = find_index_and_year(key, value)
            if year_to_index is not None:
                is_it_year_entry = True
                years.append(year_to_index)
            else:
                if TITLE == value or (is_it_year_entry and not value):
                    years.append({"value": "title", "index": key})
                    is_it_year_entry = False
                    del escaped_data[-1]
                if value in ANNOTATION:
                    years.append({"value": "annotation", "index": key})
        if is_it_year_entry:
            # TODO : Bug
            years.append({"value": "title", "index": u'5'})

    new_data = []
    for entry in escaped_data:
        number_of_values_in_row = len(entry)
        if number_of_values_in_row == len(years) or (number_of_values_in_row + 1 == len(years)):
            new_data.append(entry)
    return [new_data, years]


def remove_empty_string(dict):
    new_dictionary = {}
    regex = re.compile(r'[\(*\)\n\r\t]')
    for elem in dict.keys():
        key = regex.sub("", elem)
        value = regex.sub("", dict[elem])
        if key != None and bool(value.strip()) == True:
            new_dictionary[key] = value
    return new_dictionary


def find_index_and_year(key, value):
    regex_pattern = "(19|20)\d{2}"
    result = re.match(regex_pattern, value)
    if result:
        return {"value": value, "index": key}
    else:
        return None


if __name__ == '__main__':
    main()
