#!/bin/bash

virtualenv .env && source .env/bin/activate && pip install -r requirements.txt
cd fin_scrapy
scrapy crawl --nolog -o - -t json financestats
