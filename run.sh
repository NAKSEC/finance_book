#!/bin/bash

virtualenv .env && source .env/bin/activate && pip install -r requirements.txt
cd fin_scrapy
scrapy crawl -a ticker=AAPL --nolog -o - -t json finance

