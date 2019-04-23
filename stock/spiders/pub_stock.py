#!/bin/python
# -*- coding: UTF-8 -*-
import scrapy
from scrapy.http import Request
from stock.items.items import StockNewItem
from scrapy.utils.project import get_project_settings
import re
import json
import urllib2
# 新增股票爬虫
class Reports(scrapy.Spider):

	custom_settings = {
	    'ITEM_PIPELINES': {
		     'stock.reportspipelines.stock_pipelines.StockPipeline': 1,
		}
 	}
	name = 'add_stock'
	base_url = "http://data.eastmoney.com/xg/xg/default.html"
	def start_requests(self):
		yield Request(self.base_url,callback=self.parse)

	def parse(self,response):
		content = response.text
		pattern = re.compile(r'&token=(.*?)&')
		result = pattern.findall(content)
		json_url = 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=XGSG_LB&token=%s&p=1&ps=40' % result[0]
		yield Request(json_url,callback=self.getStock)

	# 获取股票数据
	def getStock(self,response):
		content = response.text
		content = json.loads(content)
		settings = get_project_settings()

		for elem in content:
			if elem['kb'] == '待上市':
				continue
			code = self.getExchange(elem['securitycode'])

			if code:
				item = StockNewItem()
				item['name'] = elem['securityshortname']
				item['code'] = elem['securitycode']
				item['exchange'] = code
				yield item
		settings = get_project_settings()

		urllib2.urlopen(settings.get('ADD_STOCK_PINYIN'))

	# 判断股票交易所
	def getExchange(self,code):
		code = int(code[0:1])

		if code == 6:
			return 'SS.ESA'
		elif code == 3 or code == 0:
			return 'SZ.ESA'
		else:
			return None
