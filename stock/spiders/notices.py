#!/bin/python
# -*- coding: UTF-8 -*-
import scrapy
from scrapy.http import Request
from stock.items.items import NoticesItem
from bs4 import BeautifulSoup
from stock.middlewares.common import ErrorLog
import re
import json
import urllib2
import random
import time
import datetime
import math


# 股票公告
# 爬取的数据地址：http://www.cninfo.com.cn/cninfo-new/disclosure/szse
class Notices(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES': {
            'stock.reportspipelines.notices_pipelines.NoticesPipeline': 1,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'stock.middlewares.notices.NoticesMiddlewares': 1,
        }
    }
    name = 'notices'

    # 初始化
    def __init__(self, category='szse'):
        self.category = category
        super(Notices, self).__init__()

    base_url = "http://www.cninfo.com.cn/cninfo-new/announcement/query"
    pdf_url = 'http://www.cninfo.com.cn/'
    total = -1

    # date = '2018-08-28 ~ 2018-08-31'
    # szse A股 hke 港股 neeq_company 新三板
    # category = 'neeq_company'

    def start_requests(self):
        x = 0
        while True:
            if x > self.total and self.total != -1:
                break
            else:
                x += 1
            yield scrapy.FormRequest(
                self.base_url,
                formdata={
                    'column': self.category,
                    'pageNum': str(x),
                    'pageSize': '30',
                    'seDate': self.getDate(),
                    'tabName': 'fulltext'
                },
                callback=self.parse,
                errback=self.error_handle
            )
            # break

    # 解析json
    def parse(self, response):
        content = response.text
        try:
            content = json.loads(content)
            if self.total == -1:
                self.total = math.ceil(content['totalAnnouncement'] / 30)
            for x in content['announcements']:
                # print time.strftime("%Y-%m-%d",time.localtime(int(x['announcementTime']/1000)))
                item = NoticesItem()
                item['sid'] = x['announcementId']
                item['secu_code'] = x['secCode']
                item['title'] = x['secName'] + "：" + x['announcementTitle']
                item['category'] = self.getCategory()
                item['url'] = self.pdf_url + x['adjunctUrl']
                item['date'] = time.strftime("%Y-%m-%d", time.localtime(int(x['announcementTime'] / 1000)))

                yield item
        except Exception as e:
            print(e)

    # 获取类型
    def getCategory(self):
        if self.category == 'hke':
            return 2
        elif self.category == 'szse':
            return 1
        elif self.category == 'neeq_company':
            return 3
        else:
            return 0

    # 爬取时间
    def getDate(self, num=1):
        today = datetime.date.today()
        time12 = int(time.strftime("%H"))
        if time12 <= 12:
            if time12 == 9:
                oneday = datetime.timedelta(days=int(1))
                return str(today - oneday)
            elif time12 == 10:
                oneday = datetime.timedelta(days=int(2))
                return str(today - oneday)

            elif time12 == 11:
                oneday = datetime.timedelta(days=int(3))
                return str(today - oneday)
            return str(today)
        else:
            time20 = int(time.strftime("%M"))
            if time20 <= 20 and time12 > 18:
                if time12 == 13:
                    oneday = datetime.timedelta(days=int(4))
                    return str(today - oneday)
                elif time12 == 14:
                    oneday = datetime.timedelta(days=int(5))
                    return str(today - oneday)
                return str(today)
            else:
                oneday = datetime.timedelta(days=int(num))
                return str(today + oneday)

    def error_handle(self, response):
        response.value


class NoticesNeeq(scrapy.Spider):
    '''
    http://www.neeq.com.cn/disclosure/announcement.html
    新三板数据
    '''
    custom_settings = {
        'ITEM_PIPELINES': {
            'stock.reportspipelines.notices_pipelines.NoticesPipeline': 1,
        }
    }
    name = 'notices_neeq'

    base_url = "http://www.neeq.com.cn/disclosureInfoController/infoResult.do?callback=jQuery"
    pdf_url = 'http://www.neeq.com.cn'
    page = 0
    def start_requests(self):
        startDate = self.getDate()
        yield scrapy.FormRequest(
            self.base_url,
            formdata={
                'disclosureType': '5',
                'page': '0',
                'isNewThree': self.getNewThree(),
                'startTime': startDate['startTime'],
                'endTime': startDate['endTime']
            },
            dont_filter=True
        )

    # 解析json
    def parse(self, response):
        content = response.text
        try:
            content = json.loads(content[7:-1])
            for x in content[0]['listInfo']['content']:
                title = x['disclosureTitle'].lstrip('[临时公告]')
                item = NoticesItem()
                item['sid'] = x['disclosureCode']
                item['secu_code'] = x['companyCd']
                item['title'] = title
                item['category'] = 3
                item['url'] = self.pdf_url + x['destFilePath']
                item['date'] = x['publishDate']
                yield item
            if content[0]['listInfo']['totalPages'] > self.page:
                self.page += 1
                startDate = self.getDate()
                yield scrapy.FormRequest(
                    self.base_url,
                    formdata={
                        'disclosureType': '5',
                        'page': str(self.page),
                        'isNewThree': self.getNewThree(),
                        'startTime': startDate['startTime'],
                        'endTime': startDate['endTime']
                    },
                    callback=self.parse,
                    dont_filter=True
                )
        except Exception as e:
            print e
    def getDate(self):
        '''
        获取开始和结束时间
        :return:
        '''
        today = datetime.date.today()
        oneday = datetime.timedelta(days=int(9))

        return {
            'startTime':str(today - oneday),
            'endTime': str(today)
        }
    def getNewThree(self):
        time12 = int(time.strftime("%H"))
        if time12 % 2 == 0:
            return '0'
        else:
            return '1'