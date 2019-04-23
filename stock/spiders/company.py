#!/bin/python
# -*- coding: UTF-8 -*-
import scrapy
from scrapy.http import Request
from stock.items.items import CompanyItem
from stock.model.stock import Stock
from bs4 import BeautifulSoup
import json
import time

# 公司详情爬虫
class Company(scrapy.Spider):
	custom_settings = {
	    'ITEM_PIPELINES': {
		     'stock.reportspipelines.company_pipelines.CompanyPipeline': 1,
		}
 	}
	name = 'company'
	base_url = "http://www.cninfo.com.cn/information/brief/%s.html"
	manager_url = 'http://www.cninfo.com.cn/information/management/%s.html'
	theme_url = 'http://emweb.securities.eastmoney.com/PC_HSF10/CoreConception/CoreConceptionAjax?code=%s'
	def start_requests(self):
		stock = Stock.getInstance()
		page = 0
		while True:
			page += 1
			exchnage = stock.getStockInfo(page)
			if exchnage:
				for elem in exchnage:
					code = self.produceBriefExchage(elem[1])
					if code:
						sc_url = self.base_url % code
						yield Request(sc_url,self.parse,meta={'code':elem[1]})
			else:
				break
	# 解析公司概要
	def parse(self,response):
		
		content = response.text
		soup = BeautifulSoup(content)

		content = soup.select('.clear table tr td')

		data = []
		for index,elem in enumerate(content):
			if index % 2 == 0:
				temporary = elem.string
			else:
				tem = {'key':temporary,'value':elem.string}
				data.append(tem)
		item = {
			'code':response.meta['code'],
			'profile':json.dumps(data)
		}
		code = self.produceBriefExchage(item['code'])
		if code:
			yield Request(self.manager_url % code,self.getTheme,meta=item)
	# 解析高管
	def getTheme(self,response):
		content = response.text
		soup = BeautifulSoup(content)
		content = soup.select('.clear table tr td')
		data = []
		for index,elem in enumerate(content):
			if index >= 5:
				if index % 5 == 0:
					tem = {}
					tem['name'] = elem.string
				elif index % 5 == 1:
					tem['post'] = elem.string
				elif index % 5 == 2:
					tem['age'] = elem.string
				elif index % 5 == 3:
					tem['sex'] = elem.string
				else:
					tem['education'] = elem.string
					data.append(tem)
		item = {
			'code':response.meta['code'],
			'profile':response.meta['profile'],
			'manager':json.dumps(data)
		}
		code = self.produceThemeExchage(item['code'])
		if code:
			yield Request(self.theme_url % code,self.parseItem,meta=item)

	# 解析核心概念
	def parseItem(self,response):
		meta = response.meta
		item = CompanyItem()
		item['code'] = meta['code']
		item['profile'] = meta['profile']
		item['manager'] = meta['manager']
		item['theme'] = response.text
		return item
	# 解析公司概况和高管是那个交易所
	def produceBriefExchage(self,code):
		first = int(code[0:1])
		if first == 6:
			return 'shmb'+code
		elif first == 0:
			if code[0:3] == '002':
				return 'szsme'+code
			return 'szmb'+code
		elif first == 3:
			return 'szcn'+code
		else:
			return None
	# 解析高管判断是那个交易所
	def produceThemeExchage(self,code):
		first = int(code[0:1])
		if first == 6:
			return 'SH'+code
		elif first == 0 or first == 3:
			return 'SZ'+code
		else:
			return None
