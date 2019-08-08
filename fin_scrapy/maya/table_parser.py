import csv
import json

from string_utils import *


class ValueIndexPair:
    def __init__(self, value, index):
        self.index = index
        self.value = value

    @staticmethod
    def sortByValue(obj):
        return int(obj.value)


class KnownWords:
    def __init__(self):
        self.ANNOTATION = [u'\u05e8\u05d5\u05d0\u05d1', u'\u05e8\u05d5\u05d0\u05d9\u05d1']
        self.TITLE = u'\u05e9\u05d7"  \u05d9\u05e4\u05dc\u05d0\u05d1'


class JsonTableParser:
    def __init__(self, file_path, encoding='utf8'):
        with open(file_path) as file:
            self.raw_data = json.load(file, encoding=encoding)
            self.escaped_data = []
            self.years = {}
            self.known_words = KnownWords()

    def parse(self):
        for entry in self.raw_data:
            new_entry = remove_empty_key_value_from_dictionary(entry)
            self.escaped_data.append(new_entry)
            for key, value in new_entry.items():
                new_value = self.parse_years_colunm_from_table(key, value)
                if new_value is not None:
                    new_entry[key] = new_value

        self.add_title_index_if_not_exist()

        self.append_data()

    def add_title_index_if_not_exist(self):
        if not self.years.has_key("Title"):
            bigger_number = 0
            for i in self.years.values():
                if bigger_number < int(i):
                    bigger_number = int(i)
            self.years["Title"] = unicode(bigger_number + 1)

    def append_data(self):
        new_data = []
        for entry in self.escaped_data:
            number_of_values_in_row = len(entry)
            if number_of_values_in_row == len(self.years) or (number_of_values_in_row + 1 == len(self.years)):
                new_data.append(entry)
        self.escaped_data = new_data

    def parse_years_colunm_from_table(self, index, value):
        is_it_year_entry = False
        try:
            value = ''.join(value)
            year_to_index = self.find_index_and_year(index, value)
            is_it_year_entry = True
            self.years[year_to_index.value] = year_to_index.index
            return value
        except Exception as error:
            print error
            if self.known_words.TITLE == value or (is_it_year_entry and not value):
                self.years["Title"] = index
                del self.escaped_data[-1]
            if value in self.known_words.ANNOTATION:
                self.years["Annotation"] = index
        return None

    def find_index_and_year(self, key, value):
        result = is_year_by_regex(value)
        if result:
            return ValueIndexPair(value, key)
        else:
            raise Exception("Cant find regex pattern in string : %s. key : key" % (value, key))


class CSVWriter():
    def __init__(self, json_table_object):
        self.json_table_object = json_table_object
        self.columns = []
        self.rows = []

    def create_csv_columns_and_rows(self):
        years = self.json_table_object.years

        if years.has_key("Title"):
            self.columns.append("Title")

        list_of_years = years.keys()
        only_years = []
        for x in list_of_years:
            if is_year_by_regex(x):
                only_years.append(x)

        only_years.sort(key=int)

        for x in only_years:
            self.columns.append(x)

        if years.has_key("Annotation"):
            self.columns.append("Annotation")

        for dict_data in self.json_table_object.escaped_data:
            data = []
            for i in self.columns:
                index = years[i]
                try:
                    data.append(dict_data[index].encode("utf8"))
                except Exception as e:
                    print e
            self.rows.append(data)

    def write_to_file(self, path):
        with open(path, mode='wb') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            writer.writerow(self.columns)
            for s in self.rows:
                s[0] = s[0][::-1]
                writer.writerow(s)

        # print (df)
