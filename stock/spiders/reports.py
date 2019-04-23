#!/bin/python
# -*- coding: UTF-8 -*-
import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from stock.items.items import ReportsItem, ReportsWxItem
from stock.model.stock import Stock
from scrapy.utils.project import get_project_settings
from stock.model.redis_model import RedisModel
import json
import time
import random
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import os, base64, datetime, hashlib, hmac


# 获取研报的数据：http://data.eastmoney.com/report/
class Reports(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES': {
            'stock.reportspipelines.pipelines.ReportsPipeline': 255,
        }
    }
    name = 'reports'
    bash_url = 'http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR&js=var rJfJRIOl={"data":[(x)],"pages":"(pc)","update":"(ud)","count":"(count)"}&ps=50&p=%d&mkt=0&stat=0&cmd=0&code=&rt=51158484'
    pageTotal = 2

    def start_requests(self):
        # for i in xrange(1,10):
        # 	url = self.bash_url
        # yield Request(self.bash_url % '000656',self.parse)
        stock = Stock.getInstance()
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
                publ_date = time.strptime(elem['datetime'], '%Y-%m-%dT%H:%M:%S')
                datetime = time.strftime('%Y%m%d', publ_date)

                # 只同步当天的研报，提高性能
                # if datetime != time.strftime('%Y%m%d'):
                # 	continue

                content_url = 'http://data.eastmoney.com/report/%s/%s.html' % (datetime, elem['infoCode'])
                meta = {
                    'title': elem['title'],
                    'secu_code': elem['secuFullCode'][:elem['secuFullCode'].find('.')],
                    'sid': elem['infoCode'],
                    'invest_statement': elem['sratingName'],
                    'org_name': elem['insName'],
                    'publ_date': time.strftime('%Y-%m-%d', publ_date)
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
            # print()
            content = response.xpath('//div[@class="newsContent"]').extract_first()
            pdf = response.xpath('//div[@class="report-infos"]/span/a/@href').extract()
            pdf = pdf[1]
        except Exception as e:
            pdf = ''

        item = ReportsItem()
        item['url'] = pdf
        item['conclusion'] = content
        item['title'] = meta['title']
        item['secu_code'] = meta['secu_code']
        item['sid'] = meta['sid']
        item['invest_statement'] = meta['invest_statement']
        item['org_name'] = meta['org_name']
        item['publ_date'] = meta['publ_date']

        return item


class ReportsWx(scrapy.Spider):
    '''
    爬取微信公众号研报
    '''
    org_name = '国投安信期货'
    name = 'reports_wx'
    # custom_settings = {
    # 	# 'ITEM_PIPELINES': {
    # 	# 	'stock.reportspipelines.legal_pipelines.LegalPipeline': 10,
    # 	# },
    # 	'DOWNLOADER_MIDDLEWARES': {
    # 		'stock.middlewares.reports.ReportsWxMiddlewares': 255,
    # 	}
    # }
    start_urls = [
        'https://mp.weixin.qq.com/'
    ]

    @classmethod
    def update_settings(cls, settings):
        sett = get_project_settings()
        item = settings.get('DOWNLOADER_MIDDLEWARES')
        custom_settings = {
            'DOWNLOADER_MIDDLEWARES': {
                'stock.middlewares.reports.ReportsWxMiddlewares': 255,
            },
            'ITEM_PIPELINES': {
                'stock.reportspipelines.pipelines.ReportsWxPipeline': 255,
            }
        }
        for k, v in item.items():
            custom_settings['DOWNLOADER_MIDDLEWARES'][k] = v
        cls.custom_settings = custom_settings
        settings.setdict(cls.custom_settings or {}, priority='spider')

    def parse(self, response):

        token = re.findall(r'token=(\d+)', str(response.url))[0]

        query_id = {
            'action': 'list_ex',
            'token': str(token),
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': str(random.random()),
            'query': '',
            'begin': '0',
            'count': '5',
            # 'fakeid': 'MzUxMjI3OTk2OA==',
            'fakeid': 'MjM5NTcxNDUwMQ==',
            'type': '9'

        }
        search_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg'
        for begin in xrange(0, 1045, 5):
            query_id['begin'] = str(begin)
            time.sleep(3)
            yield scrapy.FormRequest(
                url=search_url,
                callback=self.getArticleList,
                method='GET',
                formdata=query_id
            )

    def getArticleList(self, response):
        items = json.loads(response.text)
        if items.get('app_msg_list'):
            for item in items.get('app_msg_list'):
                # print item['title']
                meta = {
                    'title': item['title'],
                    'sid': item['aid'],
                    'pdate': time.strftime("%Y-%m-%d", time.localtime(item['update_time']))
                }
                time.sleep(3)
                yield Request(item['link'], callback=self.getArticle, meta=meta)
        else:
            begin = re.findall(r'begin=(\d+)', str(response.url))[0]
            print response.url
            print begin
            print '访问失败'

    def getArticle(self, response):
        '''
        获取文章内容详情
        :param response:
        :return:
        '''
        meta = response.meta

        item = ReportsWxItem()
        item['title'] = meta['title']
        item['sid'] = meta['sid']
        item['org_name'] = self.org_name
        item['pdate'] = meta['pdate']
        item['content'] = response.text

        yield item


class ReportsWxSogou(scrapy.Spider):
    '''
    爬取微信公众号研报
    https://weixin.sogou.com
    '''
    org_name = '国投安信期货'
    queryDist = {
        "CIB_Research_MacEcon": "兴业研究"
    }
    name = 'reports_wx_sogou'

    # custom_settings = {
    # 	# 'ITEM_PIPELINES': {
    # 	# 	'stock.reportspipelines.legal_pipelines.LegalPipeline': 10,
    # 	# },
    # 	'DOWNLOADER_MIDDLEWARES': {
    # 		'stock.middlewares.reports.ReportsWxMiddlewares': 255,
    # 	}
    # }
    # start_urls = [
    #     'https://mp.weixin.qq.com/'
    # ]

    @classmethod
    def update_settings(cls, settings):
        sett = get_project_settings()
        item = settings.get('DOWNLOADER_MIDDLEWARES')
        custom_settings = {
            'DOWNLOADER_MIDDLEWARES': {
                'stock.middlewares.reports.ReportsWxSogouMiddlewares': 255,
            },
            # 'ITEM_PIPELINES': {
            #     'stock.reportspipelines.pipelines.ReportsWxPipeline': 255,
            # }
        }
        for k, v in item.items():
            custom_settings['DOWNLOADER_MIDDLEWARES'][k] = v
        cls.custom_settings = custom_settings
        settings.setdict(cls.custom_settings or {}, priority='spider')

    def start_requests(self):
        url = "https://weixin.sogou.com/weixin?type=1&s_from=input&query=CIB_Research_MacEcon&ie=utf8&_sug_=n&_sug_type_="
        query = re.findall(r'query=(\w+)&', str(url))[0]
        print query
        yield Request(url, callback=self.parse)

    def parse(self, response):
        articel_list_url = response.xpath('//div[@class="txt-box"]/p/a/@href').extract_first()
        print response.url
        if articel_list_url:
            yield Request(articel_list_url, callback=self.getArticleList, meta=meta)
        else:
            print articel_list_url
            print "失败"

    def getArticleList(self, response):
        pass
        # items = json.loads(response.text)
        print response.text

    def getArticle(self, response):
        '''
        获取文章内容详情
        :param response:
        :return:
        '''
        meta = response.meta

        item = ReportsWxItem()
        item['title'] = meta['title']
        item['sid'] = meta['sid']
        item['org_name'] = self.org_name
        item['pdate'] = meta['pdate']
        item['content'] = response.text

        yield item


class ReportsWxGs(scrapy.Spider):
    '''
    爬取微信公众号研报
    https://weixin.sogou.com
    '''
    org_name = '国投安信期货'
    queryDist = {
        "CIB_Research_MacEcon": "兴业研究"
    }
    name = 'reports_wx_gs'

    method = 'GET'
    service = '/weixin/v1/articles'
    host = 'api.gsdata.cn'
    request_parameters = 'wx_name=rmrbwx'
    app_id = "1381"
    secret_key = "_sJmdmi23ccTK9KIwCgVlqZ7HOBgnUd3"

    # custom_settings = {
    # 	# 'ITEM_PIPELINES': {
    # 	# 	'stock.reportspipelines.legal_pipelines.LegalPipeline': 10,
    # 	# },
    # 	'DOWNLOADER_MIDDLEWARES': {
    # 		'stock.middlewares.reports.ReportsWxMiddlewares': 255,
    # 	}
    # }
    # start_urls = [
    #     'https://mp.weixin.qq.com/'
    # ]

    # @classmethod
    # def update_settings(cls, settings):
    #     sett = get_project_settings()
    #     item = settings.get('DOWNLOADER_MIDDLEWARES')
    #     custom_settings = {
    #         'DOWNLOADER_MIDDLEWARES': {
    #             'stock.middlewares.reports.ReportsWxSogouMiddlewares': 255,
    #         },
    #         # 'ITEM_PIPELINES': {
    #         #     'stock.reportspipelines.pipelines.ReportsWxPipeline': 255,
    #         # }
    #     }
    #     for k, v in item.items():
    #         custom_settings['DOWNLOADER_MIDDLEWARES'][k] = v
    #     cls.custom_settings = custom_settings
    #     settings.setdict(cls.custom_settings or {}, priority='spider')

    def start_requests(self):
        t = datetime.datetime.utcnow()
        gsdate = t.strftime('%Y%m%dT%H%M%SZ')
        datestamp = t.strftime('%Y%m%d')  # Date w/o time, used in credential scope

        canonical_uri = self.service
        canonical_querystring = self.request_parameters
        canonical_headers = 'host:' + self.host + '\n' + 'x-gsdata-date:' + gsdate

        signed_headers = 'host;x-gsdata-date'
        payload_hash = hashlib.sha256(''.encode("utf8")).hexdigest()
        canonical_request = self.method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
        algorithm = 'GSDATA-HMAC-SHA256'
        string_to_sign = algorithm + '\n' + gsdate + '\n' + hashlib.sha256(canonical_request.encode("utf8")).hexdigest()

        signing_key = self.getSignatureKey(self.secret_key, datestamp, self.service)

        signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()
        authorization_header = algorithm + ' ' + 'AppKey=' + self.app_id + ', ' + 'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
        headers = {'x-gsdata-date': gsdate, 'Authorization': authorization_header, "Accept": "text/html,application/json;q=0.9,image/webp,image/apng,*/*;q=0.8"}

        request_url = 'http://' + self.host + self.service + '?' + canonical_querystring

        print '\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++'
        print 'Request URL = ' + request_url

        yield Request(request_url, callback=self.parse, headers=headers)

        print '\nRESPONSE++++++++++++++++++++++++++++++++++++'

    def sign(self, key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

    def getSignatureKey(self, key, dateStamp, serviceName):
        kDate = self.sign(('GSDATA' + key).encode('utf-8'), dateStamp)
        kService = self.sign(kDate, serviceName)
        kSigning = self.sign(kService, 'gsdata_request')
        return kSigning

    def parse(self, response):
        print response.url
        print json.dumps(response.text)

    def getArticleList(self, response):
        pass
        # items = json.loads(response.text)
        print response.text

    def getArticle(self, response):
        '''
        获取文章内容详情
        :param response:
        :return:
        '''
        meta = response.meta

        item = ReportsWxItem()
        item['title'] = meta['title']
        item['sid'] = meta['sid']
        item['org_name'] = self.org_name
        item['pdate'] = meta['pdate']
        item['content'] = response.text

        yield item
