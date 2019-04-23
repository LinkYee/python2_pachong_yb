#!/bin/python
# -*- coding: UTF-8 -*-
import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from stock.items.items import ReportsHyItem, ReportsOrgItem
from stock.model.stock import Stock
import json
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


# 获取行业研报的数据：http://data.eastmoney.com/report/hyyb.html#dHA9MCZjZz0wJmR0PTQmcGFnZT0y
class ReportsIndustry(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES': {
            'stock.reportspipelines.pipelines.ReportsHyPipeline': 255,
        }
    }
    name = 'reports_macro'
    bash_url = 'http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=HGYJ&cmd=4&code=&ps=50&p=%d&js=var TCiOyLKI={"data":[(x)],"pages":"(pc)","update":"(ud)","count":"(count)"}&rt=51224729'
    pageTotal = 315

    def start_requests(self):
        # for i in xrange(1,10):
        # 	url = self.bash_url
        # yield Request(self.bash_url % '000656',self.parse)
        # stock = Stock.getInstance()
        page = 0
        while True:
            page += 1

            if self.pageTotal != -1 and page > self.pageTotal:
                break
            else:
                sc_url = self.bash_url % page
                yield Request(sc_url, callback=self.parse)
            # break

    def parse(self, response):
        try:
            content = response.body_as_unicode()
            content = json.loads(content[13:])
            if self.pageTotal == -1:
                self.pageTotal = content['pages']

            for elem in content['data']:
                data = elem.split(',')

                publ_date = time.strptime(data[0], '%Y/%m/%d %H:%M:%S')
                datetime = time.strftime('%Y%m%d', publ_date)

                # 只同步当天的研报，提高性能
                # if datetime != time.strftime('%Y%m%d'):
                # 	continue

                content_url = 'http://data.eastmoney.com/report/%s/hg,%s.html' % (datetime, data[1])
                meta = {
                    'title': data[5],
                    'name': '宏观研究',
                    'sid': data[1],
                    'invest_statement': '',
                    'org_name': data[3],
                    'pdate': time.strftime('%Y-%m-%d', publ_date)
                }

                yield Request(content_url, callback=self.getContent, meta=meta)

        except Exception as e:
            print(e)

    # 获取内容数据
    def getContent(self, response):
        meta = response.meta

        try:
            # soup = BeautifulSoup(response.text)
            # pdf = soup.select('div.report-infos span a')
            content = response.xpath('//div[@class="newsContent"]').extract_first()
            pdf = response.xpath('//div[@class="report-infos"]/span/a/@href').extract()

            pdf = pdf[1]
        except Exception as e:
            pdf = ''

        item = ReportsHyItem()
        item['url'] = pdf
        item['content'] = content
        item['name'] = meta['name']
        item['title'] = meta['title']
        item['sid'] = meta['sid']
        item['invest_statement'] = meta['invest_statement']
        item['org_name'] = meta['org_name']
        item['pdate'] = meta['pdate']

        return item


# 获取艾瑞行业研报的数据：http://www.iresearch.com.cn/Research/IndustryList.shtml
class ReportsIre(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES': {
            'stock.reportspipelines.pipelines.ReportsOrgPipeline': 255,
        }
    }
    name = 'reports_ire'
    bash_url = 'http://www.iresearch.com.cn/products/GetReportList?classId=&fee=0&date=&lastId=&pageSize=10'

    def start_requests(self):

        yield Request(self.bash_url, callback=self.parse)

    def parse(self, response):
        try:
            content = response.body_as_unicode()
            content = json.loads(content)

            for elem in content['List']:
                publ_date = time.strptime(elem['Uptime'], '%Y/%m/%d %H:%M:%S')

                item = ReportsOrgItem()
                item['url'] = 'http://www.iresearch.cn/include/ajax/user_ajax.ashx?work=idown&rid=%d' % elem['NewsId']
                item['content'] = ''
                item['name'] = elem['industry']
                item['title'] = elem['Title']
                item['sid'] = elem['Id']
                item['invest_statement'] = ''
                item['label_name'] = ','.join(elem['Keyword'])
                item['org_name'] = elem['Author']
                item['pdate'] = time.strftime('%Y-%m-%d', publ_date)
                yield item

        except Exception as e:
            print(e)

