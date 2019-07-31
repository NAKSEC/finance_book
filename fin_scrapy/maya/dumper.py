#!/usr/bin/env python
# -*- coding: utf-8 -*-

import camelot


def main():
    tables = camelot.read_pdf('NOTKPMG.pdf', pages='84', flavor='stream')
    # print tables
    tables.export("json", f='json')


if __name__ == '__main__':
    main()
