#!/bin/python
# -*- coding: UTF-8 -*-
import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from stock.items.items import InvestmentItem
import sys
import math
import urlparse

reload(sys)
sys.setdefaultencoding('utf-8')


# 获取行业研报的数据：http://data.eastmoney.com/report/hyyb.html#dHA9MCZjZz0wJmR0PTQmcGFnZT0y
class InvestmentAsk(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES': {
            'stock.reportspipelines.investment_pipelines.InvestmentPipeline': 255,
        }
    }
    name = 'investment_ask'
    bash_url = 'http://www.thxflt.com/bestanswer.php?mod=huzhu&type=do&page=%d'

    def start_requests(self):
        # yield Request(self.bash_url % 1, callback=self.getAskList)
        page = 233
        for num in range(1, int(page) + 1):
            yield Request(self.bash_url % num, callback=self.getAskList)
        # yield Request(self.bash_url % 1, callback=self.parse)

    def parse(self, response):

        # page = response.xpath('//div[@id="pagediv"]//div[@class="pg"]//label//span//text()').extract_first()
        # page[3:-2]
        page = 2
        for num in range(2, int(page) + 1):
            yield Request(self.bash_url % num, callback=self.getAskList)

    def getAskList(self, response):
        '''
        获取问答列表
        :param response:
        :return:
        '''

        content = response.xpath('//div[@id="pagediv"]//table//tr').extract()
        for elem in content:
            # print elem
            soup = BeautifulSoup(elem)
            content_url = soup.find_all('a')[1].get('href')
            # content_url = 'http://www.thxflt.com/forum.php?mod=viewthread&tid=567703&extra=page%3D1'
            yield Request(content_url, callback=self.getAskContent)
            # break
            # ask_num = soup.find_all('td')[1].font.string
            # ask_date = soup.find_all('td')[2].font.string
            # print(ask_date)

    # 获取内容数据
    def getAskContent(self, response):
        content = response.xpath('//div[@id="postlist"]/div').extract()
        category = response.xpath('//div[@id="pt"]//div[@class="z"]//a//text()').extract()[3]
        category = category.strip("【")
        category = category.strip("】")

        title = response.xpath('//span[@id="thread_subject"]//text()').extract()[1]
        reply_num = int(response.xpath('//span[@class="xi1"]//text()').extract()[1])
        tid = urlparse.parse_qs(urlparse.urlparse(response.url).query)['tid'][0]
        for key, val in enumerate(content):
            soup = BeautifulSoup(val)
            post_id = soup.div.get('id')
            if post_id != 'postlistreply':
                if key == 0:
                    xw1 = soup.find(class_='xw1')
                    if xw1:
                        name = xw1.string
                    else:
                        name = '匿名'

                    post_id = post_id.split('_')
                    postmessage = 'postmessage_' + post_id[1]
                    authorposton = 'authorposton' + post_id[1]

                    pdate = soup.find(id=authorposton).get_text()
                    if pdate[-1:] == '前':
                        pdate = soup.find(id=authorposton).find('span').attrs['title']
                    else:
                        pdate = pdate[4:].strip()
                    [s.decompose() for s in soup.select('.t_f div')]
                    [s.decompose() for s in soup.select('.t_f style')]

                    item = InvestmentItem()
                    item['type'] = 0
                    item['title'] = title
                    item['category'] = category
                    item['sid'] = tid
                    item['name'] = name
                    item['pdate'] = pdate
                    item['content'] = soup.find(id=postmessage).decode_contents().strip()
                    item['reply_num'] = reply_num
                    yield item
                else:
                    # if key ==1:
                    #     continue
                    xw1 = soup.find(class_='xw1')
                    if xw1:
                        name = xw1.string
                    else:
                        name = '匿名'
                    post_id = post_id.split('_')
                    postmessage = 'postmessage_' + post_id[1]
                    authorposton = 'authorposton' + post_id[1]

                    pdate = soup.find(id=authorposton).get_text()
                    if pdate[-1:] == '前':
                        pdate = soup.find(id=authorposton).find('span').attrs['title']
                    else:
                        pdate = pdate[4:].strip()
                    best = soup.select('.authi font')
                    a_pr = soup.find(class_='a_pr')
                    content = ''
                    if a_pr:
                        a_pr.decompose()

                    content = soup.find(id=postmessage)
                    item = InvestmentItem()
                    item['type'] = 1
                    if len(best):
                        item['best'] = 1
                    else:
                        item['best'] = 0
                    item['pdate'] = pdate
                    item['name'] = name
                    item['sid'] = tid
                    item['content'] = content
                    yield item

        if reply_num > 0:
            page = int(math.ceil(reply_num / 10.0))
            for p in range(2, page + 1):

                yield Request(response.url + "&page=" + str(p), callback=self.getAskContentNext)

    def getAskContentNext(self, response):
        content = response.xpath('//div[@id="postlist"]/div').extract()

        tid = urlparse.parse_qs(urlparse.urlparse(response.url).query)['tid'][0]
        for val in content:
            soup = BeautifulSoup(val)
            post_id = soup.div.get('id')
            if post_id != 'postlistreply':

                xw1 = soup.find(class_='xw1')
                if xw1:
                    name = xw1.string
                else:
                    name = '匿名'
                post_id = post_id.split('_')
                postmessage = 'postmessage_' + post_id[1]
                authorposton = 'authorposton' + post_id[1]

                pdate = soup.find(id=authorposton).get_text()
                if pdate[-1:] == '前':
                    pdate = soup.find(id=authorposton).find('span').attrs['title']
                else:
                    pdate = pdate[4:].strip()
                best = soup.select('.authi font')
                a_pr = soup.find(class_='a_pr')
                if a_pr:
                    a_pr.decompose()
                content = soup.find(id=postmessage)

                item = InvestmentItem()
                item['type'] = 1
                if len(best):
                    item['best'] = 1
                else:
                    item['best'] = 0
                item['pdate'] = pdate
                item['name'] = name
                item['sid'] = tid
                item['content'] = content
                yield item
