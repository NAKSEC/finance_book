#!/bin/bash
docker run -d -p 27017-27019:27017-27019 --name mongodb mongo:4.0.4
virtualenv --python=python2.7 .env && source .env/bin/activate && pip install -r requirements.txt
cd fin_scrapy
scrapy crawl -a tickers=AAPL --nolog -o - -t json finance

