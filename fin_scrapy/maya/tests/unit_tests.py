import datetime
import os
import random
import shutil
import subprocess
import sys
import unittest

sys.path.append("../")
from table_parser import *

from bson.objectid import ObjectId


class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return o.__dict__


class DumperTests(unittest.TestCase):
    def get_random_int(self, min=0, max=sys.maxint):
        return random.randint(min, max)

    def test_dumper(self):
        sys.path.append("../")
        dir = "pdf_examples"
        list_dir = os.listdir(dir)
        file_page_dict = {"example.pdf": 60, "KPMG2.pdf": 58, "KPMG3.pdf": 399, "NOTKPMG.pdf": 84}
        key_value = []
        for file in list_dir:
            head, tail = os.path.split(file)
            formated_string = os.path.join(dir, file) + "=" + str(file_page_dict[tail]) + " "
            key_value.append(formated_string)

        pdf_params = "".join(key_value)
        output_dir = "out"
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        process_command = "pythonw ../dumper.py -output %s -key_pairs %s" % (output_dir, pdf_params)
        subprocess.call(process_command, shell=True)

        files = os.listdir(output_dir)
        self.assertEqual(len(files), len(file_page_dict), "Number of files doesnt appropriate to number of pdfs")
        for file in files:
            self.assertGreater(os.stat(os.path.join(output_dir, file)).st_size, 0, ("the file didnt parsed %s", file))


class TableParserTests(unittest.TestCase):
    def get_random_int(self, min=0, max=sys.maxint):
        return random.randint(min, max)

    def test_writer(self):
        sys.path.append("../")
        dir = "out"
        list_dir = os.listdir(dir)
        output_dir = os.path.join(dir, "csv")
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)

        os.mkdir(output_dir)

        for file in list_dir:
            head, tail = os.path.split(file)
            j = JsonTableParser(os.path.join(dir, file))
            j.parse()
            c = CSVWriter(j)
            c.create_csv_columns_and_rows()

            csv_path = os.path.join(output_dir, tail + ".csv")
            c.write_to_file(csv_path)


if __name__ == '__main__':
    unittest.main()
