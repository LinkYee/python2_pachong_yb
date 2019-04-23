#!/bin/python
# coding:utf8

from stock.model.reports import *
from stock.model.stock import Stock


class ReportsPipeline(object):
    """把获取的研报保存到数据库里"""
    exchnageMap = {}

    def process_item(self, item, spider):
        reports = Reports.getInstance()
        if ReportsPipeline.exchnageMap.has_key(item['secu_code']):
            exchnage = ReportsPipeline.exchnageMap[item['secu_code']]
        else:
            stock = Stock.getInstance()
            exchnage = stock.getExchange(item['secu_code'])
            ReportsPipeline.exchnageMap[item['secu_code']] = exchnage
        item['secu_code'] = exchnage
        if exchnage and reports.isExist(item['sid'], item['secu_code']):
            reports.insert(item)


class ReportsHyPipeline(object):
    '''行业研报'''

    def process_item(self, item, spider):
        reports = ReportsHy.getInstance()

        if reports.isExist(item['sid']):
            reports.insert(item)

class ReportsOrgPipeline(object):
    '''机构行业研报'''

    def process_item(self, item, spider):
        reports = ReportsOrg.getInstance()

        if reports.isExist(item['sid']):
            reports.insert(item)
class ReportsWxPipeline(object):
    '''微信公告研报文章'''

    def process_item(self, item, spider):
        reports = ReportsWx.getInstance()

        if reports.isExist(item['sid']):
            reports.insert(item)