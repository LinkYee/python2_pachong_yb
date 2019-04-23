#!/bin/python
# -*- coding: UTF-8 -*-
import scrapy
from scrapy.http import Request
from stock.items.items import LegalItem, LegalCaseItem
from bs4 import BeautifulSoup
from stock.middlewares.common import ErrorLog
import re
import json
import urllib2
import random
import time
from stock.model.legal import LegalModel


# 法律法规
# 爬取的数据地址：http://www.valueonline.cn/laws/laws.html
class Finance(scrapy.Spider):
    custom_settings = {
        # 'ITEM_PIPELINES': {
        #     'stock.reportspipelines.legal_pipelines.LegalPipeline': 10,
        # },
        'DOWNLOADER_MIDDLEWARES': {
            'stock.middlewares.legal.LegalMiddlewares': 10,
        }
    }
    name = 'legal'
    base_url = "http://www.valueonline.cn/laws/laws/lawsManage"
    content_url = 'http://www.valueonline.cn/laws/view/%s.html#'

    def start_requests(self):
        for x in xrange(1, 2):
            yield scrapy.FormRequest(
                self.base_url,
                formdata={
                    'id': '99',
                    'pageNo': str(x),
                    'pageSize': '20',
                },
                callback=self.parse,
                errback=self.error_handle
            )

    def parse(self, response):
        content = response.body_as_unicode()

        content = json.loads(content)
        for elem in content['result']['lawsManageList']:
            legal = LegalModel.getInstance()
            # if legal.isExist(elem['id']):
            #     print elem['id']
            #     print legal.isExist(elem['id'])
            if legal.isExist(elem['id']):
                mold = (elem['lawSign'] if elem['lawSign'] else '')
                meta = {
                    'title': elem['lawsName'],
                    'mold': mold,
                    'pdate': elem['published'],
                    'enact': elem['lawSourceName'],
                    'sid': elem['id']
                }
                yield Request(self.content_url % elem['id'], callback=self.getContent, meta=meta)
        # break

    def getContent(self, response):
        meta = response.meta
        content = response.text
        soup = BeautifulSoup(content)
        soup.prettify()
        [s.extract() for s in soup('img')]
        catalog = soup.find('div', class_='de_nav_list')
        invalid = soup.find('span', id='invalid')
        content = soup.find('div', id='level0')
        itemList = soup.find('div', id='itemList')
        cateList = soup.select('#lawDeclareList a')
        category = ''
        for x in cateList:
            category += x.string + ','
        attention = soup.select("#attachList li a")
        attachmentList = ''
        for elem in attention:
            attachmentList = attachmentList + elem.string + "||" + elem.get('href') + ','
        attachmentList = (attachmentList if attachmentList == '' else attachmentList.rstrip(','))

        item = LegalItem()
        item['title'] = meta['title']
        item['enact'] = meta['enact']
        item['sid'] = meta['sid']
        item['mold'] = meta['mold']
        item['pdate'] = meta['pdate']
        item['catalog'] = catalog
        item['attachment'] = attachmentList
        item['category'] = category.rstrip(',')

        item['content'] = "%s%s" % (content, itemList)

        if invalid.text == '现行有效':
            item['status'] = 0
        elif invalid.text == '待生效':
            item['status'] = 2
        else:
            item['status'] = 1

        return item

    # 错误请求
    def error_handle(self, response):
        ErrorLog.saveError(self.name, response.value)



class LegalCase(scrapy.Spider):
    '''
    法规案例爬取：http://www.csrc.gov.cn
    '''
    custom_settings = {
        'ITEM_PIPELINES': {
            'stock.reportspipelines.legal_pipelines.LegalCasePipeline': 100,
        }
    }
    name = 'legal_case'
    start_urls = [
        'http://www.csrc.gov.cn/pub/zjhpublic/3300/3619/index_7401.htm',
        'http://www.csrc.gov.cn/pub/zjhpublic/3300/3313/index_7401.htm'
    ]
    #
    # def start_requests(self):
    #     csrc_url = 'http://www.csrc.gov.cn/pub/zjhpublic/3300/3313/index_7401_%d.htm'
    #     for e in range(60):
    #         if e == 0:
    #             yield Request("http://www.csrc.gov.cn/pub/zjhpublic/3300/3313/index_7401.htm", self.parse)
    #         else:
    #             yield Request(csrc_url % e, self.parse)
    host_url = 'http://www.csrc.gov.cn/pub/zjhpublic/'
    def parse(self,response):
        content = response.xpath('//div[@id="documentContainer"]/div[@class="row"]/li[@class="mc"]/div/a/@href').extract()
        for elem in content:

            content_url =  self.host_url + elem.lstrip('../../')
            yield Request(content_url, self.getContent)

    def getContent(self, response):
        content = response.xpath('//table[@id="headContainer"]/tbody/tr/td/table/tr/td')
        item = LegalCaseItem()
        for elem in content:
            key = elem.css('b::text').extract_first()
            value = elem.css("span::text").extract_first()
            if key == '分类:':
                value =  elem.css("span::text").extract_first()
                valueArr = [x.strip() for x in value.split(';')]
                item['category'] = ','.join(valueArr)
            elif key == '发布机构:':
                value = elem.css("span::text").extract_first()
                item['org_name'] =  value.strip() if value else ''
            elif key == '发文日期:':
                value = elem.css("span::text").extract_first().strip()
                publ_date = time.strptime(str(value), '%Y年%m月%d日')
                datetime = time.strftime('%Y-%m-%d', publ_date)
                item['pdate'] = datetime
            elif key == '文　　号:':
                value = elem.css("span::text").extract_first()
                item['reference_num'] = value.strip()
        content_url = response.url
        item['sid'] = content_url[content_url.rfind('/')+1:-4]
        item['title'] = response.xpath('//span[@id="lTitle"]/text()').extract_first()
        item['content'] = response.xpath('//div[@id="ContentRegion"]').extract_first()
        yield item






