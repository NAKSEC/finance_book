# -*- coding: utf-8 -*-
import scrapy

class FinanceStatsSpider(scrapy.Spider):
    name = 'financestats'
    allowed_domains = ['finance.yahoo.com']
    start_urls = ['http://finance.yahoo.com/quote/%5EGSPC?p=^GSPCf/']

    def start_requests(self):
        urls = [
            'https://finance.yahoo.com/quote/AAPL/financials?p=AAPL',
            'https://finance.yahoo.com/quote/AAPL/balance-sheet?p=AAPL',
            'https://finance.yahoo.com/quote/AAPL/cash-flow?p=AAPL'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for row in response.xpath('//table//tbody//tr'):
            print {
                row.xpath('td[1]//text()').extract_first(): {row.xpath('td[2]//text()').extract_first(),
                                                             row.xpath('td[3]//text()').extract_first(),
                                                             row.xpath('td[4]//text()').extract_first(),
                                                             row.xpath('td[5]//text()').extract_first()}
            }


