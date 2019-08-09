#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys

import camelot
from file_system_watcher import *


def create_json_file_from_pdf(pdf_path, file_start_with, page_number, flavor='stream'):
    watcher = FileSystemWatcher(os.getcwd(), file_start_with)
    try:
        tables = camelot.read_pdf(pdf_path, pages=page_number, flavor=flavor)
        tables.export(file_start_with, f='json')

    except Exception as e:
        print(e)
    return watcher.get_diff()


class StoreDictKeyPair(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        self._nargs = nargs
        super(StoreDictKeyPair, self).__init__(option_strings, dest, nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        my_dict = {}
        # print "values: {}".format(values)
        for kv in values:
            k, v = kv.split("=")
            my_dict[k] = v
        setattr(namespace, self.dest, my_dict)



def main(dict_pdf_page, output_directory):
    for path, page in dict_pdf_page.items():
        try:
            head, tail = os.path.split(path)
            file_start_with = ("json-%s" % tail.split(".")[0])
            files = create_json_file_from_pdf(path, file_start_with, page)
            move_files_to_output_directory(files, output_directory)
        except Exception as e:
            print(e)

    print("file : %s, pdf : %s" % (files, path))



if __name__ == '__main__':
    print("current direcory %s" % sys.path)
    parser = argparse.ArgumentParser(description='Dump table from page in a pdf to json file')
    parser.add_argument("-key_pairs", dest="my_dict", action=StoreDictKeyPair, nargs="+", metavar="KEY=VAL",
                        help='example : pdf_path1=page, pdf_path2=page ...')
    parser.add_argument("-output_dir", dest="output_directory", type=str,
                        help='Output directory to write files')

    args = parser.parse_args(sys.argv[1:])
    print("start to parse : %s \r\n" % args)
    main(args.my_dict, args.output_directory)
