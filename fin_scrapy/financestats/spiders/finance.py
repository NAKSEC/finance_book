# -*- coding: utf-8 -*-
import json
from collections import OrderedDict

import scrapy

import utils
from mongohandler import *

DOCUMENT_STOCKS = "stocks"
DOCUMENT_BALANCE_SHEET = "balance_sheet"
DOCUMENT_CASH_FLOW = "cash_flow"
MONGO_ADDRESS = 'mongodb://localhost:27017/'

MONGO_CONNECTION = Mong_Client_Wrapper(MONGO_ADDRESS)




class FinanceClassicSpider(scrapy.Spider):
    def __init__(self, ticker):
        self.ticker_stock = ticker

    name = 'finance'
    allowed_domains = ['finance.yahoo.com']

    def start_requests(self):
        print (self.ticker_stock)
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
        other_details_json_link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&" \
                                  "lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend" \
                                  "%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics" \
                                  "%2CcalendarEvents%2CsummaryDetail%2Cprice%2CincomeStatementHistory" \
                                  "%2CcashflowStatementHistory" \
                                  "%2CbalanceSheetHistory&corsDomain=finance.yahoo.com".format(
            self.ticker_stock)

        summary_table = response.xpath('//div[contains(@data-test,"summary-table")]//tr')
        request = self.yield_request(other_details_json_link, self.parse_json, summary_table)
        yield request

    @staticmethod
    def parse_table_stats(response):
        print "in parse table stats"
        context = response.meta['context']
        rows = response.xpath('//table//tr')
        for row in rows[1:]:
            data = {
                row.xpath('td[1]//text()').extract_first(): {row.xpath('td[2]//text()').extract_first(),
                                                             row.xpath('td[3]//text()').extract_first(),
                                                             row.xpath('td[4]//text()').extract_first(),
                                                             row.xpath('td[5]//text()').extract_first()}

            }
        context["summary_data"].update(data)
        utils.del_none_values_in_json(context["summary_data"])

        insert_data_into_mongo(context)
        return context

    def format_earnings_list(self, earnings_raw):
        datelist = []
        for i in earnings_raw['earningsDate']:
            datelist.append(i['fmt'])
        earnings_date = ' to '.join(datelist)
        return earnings_date

    def parse_dom_table(self, table):
        summary_data = OrderedDict()
        for table_data in table:
            raw_table_key = table_data.xpath('.//td[contains(@class,"C(black)")]//text()').extract_first()
            raw_table_value = table_data.xpath('.//td[contains(@class,"Ta(end)")]//text()').extract_first()
            table_key = ''.join(raw_table_key).strip()
            table_value = ''.join(raw_table_value).strip()
            summary_data.update({table_key: table_value})
        return summary_data

    def parse_balance_sheet(self, json_raw_result):
        balance_sheet = json_raw_result["balanceSheetHistory"]["balanceSheetStatements"][0]
        balance_sheet_data = utils.raw_json_answer_parser(balance_sheet)
        balance_sheet_data['ticker'] = self.ticker_stock
        return balance_sheet_data

    def parse_summary_data(self, json_raw_result, data, url):
        summary_detail = json_raw_result["summaryDetail"]
        summary_detail_data = utils.raw_json_answer_parser(summary_detail)

        recommendation_trend_data = utils.raw_json_answer_parser(json_raw_result["recommendationTrend"])

        price_data = utils.raw_json_answer_parser(json_raw_result["price"])
        earnings_date = self.format_earnings_list(json_raw_result["calendarEvents"]['earnings'])
        summary_data = self.parse_dom_table(data)

        summary_data.update(
            {'1y Target Est': json_raw_result["financialData"]["targetMeanPrice"]['raw'],
             'EPS (TTM)': json_raw_result["defaultKeyStatistics"]["trailingEps"]['raw'],
             'Earnings Date': earnings_date,
             'ticker': self.ticker_stock,
             'url': url})

        summary_data.update(price_data)
        summary_data.update(summary_detail_data)
        summary_data.update(recommendation_trend_data)
        return summary_data

    def parse_cash_flow_statement(self, json_raw_result):
        cash_flow_statements_list = json_raw_result["cashflowStatementHistory"]["cashflowStatements"]
        cash_flow_statement_data = []
        for cash_flow_statement_yearly in cash_flow_statements_list:
            cash_flow = utils.raw_json_answer_parser(cash_flow_statement_yearly)
            cash_flow['ticker'] = self.ticker_stock
            cash_flow_statement_data.append(cash_flow)
        return cash_flow_statement_data

    def parse_income_statement(self, json_raw_result):
        income_statement_history_list = json_raw_result["incomeStatementHistory"]["incomeStatementHistory"]
        income_statement_data = []

        for income_statement_history in income_statement_history_list:
            income_statement = utils.raw_json_answer_parser(income_statement_history)
            income_statement['ticker'] = self.ticker_stock
            income_statement_data.append(income_statement)

        return income_statement_data

    def parse_json(self, response):
        data_context = {}
        try:
            json_loaded_summary = json.loads(response.text)
            json_result = json_loaded_summary["quoteSummary"]["result"][0]

            data_context["summary_data"] = self.parse_summary_data(json_result,
                                                                   response.meta['context'],
                                                                   response.url)

            data_context["cash_flow"] = self.parse_cash_flow_statement(json_result)
            data_context["balance_sheet"] = self.parse_balance_sheet(json_result)
            data_context["income_statement"] = self.parse_income_statement(json_result)

        except Exception as e:
            print e
            print ("Failed to parse json response")

        stats_url = "https://finance.yahoo.com/quote/AAPL/key-statistics?p=%s" % (self.ticker_stock)

        request = self.yield_request(stats_url, self.parse_table_stats, data_context)
        yield request


def insert_data_into_mongo(context):
    print "insert data into mongo"
    print type(context)
    for key, value in context.items():
        print "inserted %s" % value
        if type(value) is list:
            for item in value:
                MONGO_CONNECTION.mongo_insert(key, dict(item))
        else:
            MONGO_CONNECTION.mongo_insert(key, dict(value))
