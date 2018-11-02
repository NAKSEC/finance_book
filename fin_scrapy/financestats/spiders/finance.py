# -*- coding: utf-8 -*-
import json
from collections import OrderedDict

import scrapy


class FinanceStatsSpider(scrapy.Spider):
    name = 'financestats'
    allowed_domains = ['finance.yahoo.com']
    start_urls = ['http://finance.yahoo.com/quote/%5EGSPC?p=^GSPCf/']

    def start_requests(self):
        urls = [
            'https://finance.yahoo.com/quote/AAPL/key-statistics?p=AAPL'
            # 'https://finance.yahoo.com/quote/AAPL/financials?p=AAPL',
            # 'https://finance.yahoo.com/quote/AAPL/balance-sheet?p=AAPL',
            # 'https://finance.yahoo.com/quote/AAPL/cash-flow?p=AAPL'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        rows = response.xpath('//table//tr')
        for row in rows[1:]:
            print {
                row.xpath('td[1]//text()').extract_first(): {row.xpath('td[2]//text()').extract_first(),
                                                             row.xpath('td[3]//text()').extract_first(),
                                                             row.xpath('td[4]//text()').extract_first(),
                                                             row.xpath('td[5]//text()').extract_first()}

            }


def del_none_values_in_json(json_obj):
    """
    Delete keys with the value ``None`` in a dictionary, recursively.

    This alters the input so you may wish to ``copy`` the dict first.
    """
    # For Python 3, write `list(d.items())`; `d.items()` won’t work
    # For Python 2, write `d.items()`; `d.iteritems()` won’t work
    for key, value in json_obj.items():
        if value is None:
            del json_obj[key]
        elif isinstance(value, dict):
            del_none_values_in_json(value)
        elif isinstance(value, set):
            json_obj[key].discard(None)
            try:
                json_obj[key] = json_obj[key].pop()
            except:
                pass
    return json_obj  # For convenience

class FinanceClassicSpider(scrapy.Spider):
    def __init__(self, ticker):
        self.ticker_stock = ticker

    name = 'finance'
    allowed_domains = ['finance.yahoo.com']

    def start_requests(self):
        print self.ticker_stock
        urls = [
            "http://finance.yahoo.com/quote/{0}?p={1}".format(self.ticker_stock, self.ticker_stock)
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    @staticmethod
    def yield_request(full_url, callback_func, context):
        req = scrapy.Request(url=full_url, callback=callback_func)
        req.meta['context'] = context
        return req

    def parse(self, response):
        other_details_json_link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com".format(
            self.ticker_stock)

        summary_table = response.xpath('//div[contains(@data-test,"summary-table")]//tr')
        request = self.yield_request(other_details_json_link, self.parse_json, summary_table)
        yield request

    def parse_table_stats(self, response):
        context = response.meta['context']
        rows = response.xpath('//table//tr')
        for row in rows[1:]:
            data = {
                row.xpath('td[1]//text()').extract_first(): {row.xpath('td[2]//text()').extract_first(),
                                                             row.xpath('td[3]//text()').extract_first(),
                                                             row.xpath('td[4]//text()').extract_first(),
                                                             row.xpath('td[5]//text()').extract_first()}

            }
            context.update(data)
            del_none_values_in_json(context)

        return context

    def parse_json(self, response):
        summary_data = OrderedDict()
        try:
            json_loaded_summary = json.loads(response.text)
            y_Target_Est = json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["targetMeanPrice"]['raw']
            earnings_list = json_loaded_summary["quoteSummary"]["result"][0]["calendarEvents"]['earnings']
            eps = json_loaded_summary["quoteSummary"]["result"][0]["defaultKeyStatistics"]["trailingEps"]['raw']
            datelist = []
            for i in earnings_list['earningsDate']:
                datelist.append(i['fmt'])
            earnings_date = ' to '.join(datelist)
            for table_data in response.meta['context']:
                raw_table_key = table_data.xpath('.//td[contains(@class,"C(black)")]//text()').extract_first()
                raw_table_value = table_data.xpath('.//td[contains(@class,"Ta(end)")]//text()').extract_first()
                table_key = ''.join(raw_table_key).strip()
                table_value = ''.join(raw_table_value).strip()
                summary_data.update({table_key: table_value})
            summary_data.update(
                {'1y Target Est': y_Target_Est, 'EPS (TTM)': eps, 'Earnings Date': earnings_date,
                 'ticker': self.ticker_stock,
                 'url': response.url})
        except:
            print ("Failed to parse json response")

        stats_url = "https://finance.yahoo.com/quote/AAPL/key-statistics?p=%s" % (self.ticker_stock)

        request = self.yield_request(stats_url, self.parse_table_stats, summary_data)
        yield request
