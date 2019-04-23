#!/bin/python
# -*- coding: UTF-8 -*-
import scrapy
from scrapy.http import Request
from stock.items.items import StockNewItem
from bs4 import BeautifulSoup
import re
import json
import urllib2
import random
# 财务报表爬虫
class Finance(scrapy.Spider):

	custom_settings = {
	    'DOWNLOADER_MIDDLEWARES': {
		     'stock.middlewares.finance.FinanceMiddlewares': 1,
		}
 	}
	name = 'finance'
	base_url = "http://www.cninfo.com.cn/information/stock/financialreport_.jsp?stockCode=600600&key=0.0017658503140858262"
	def start_requests(self):
		# for i in xrange(1,10):
		# 	url = self.bash_url
		# print(random.random())
		# random_num = random.random()
		sc_url = 'http://www.cninfo.com.cn/information/financialreport/szmb000001.html'
		yield Request(sc_url,self.parse)

		# headers={
  #           'Accept': '*/*',
  #           'Accept-Encoding': 'gzip, deflate, br',
  #           'Accept-Language': 'zh-CN,zh;q=0.9',
  #           'Connection': 'keep-alive',
  #           'Content-Length': '320',
  #           'Content-Type': "application/x-www-form-urlencoded",
  #           'Host': 'www.cninfo.com.cn',
  #           'Origin': 'https://www.cninfo.com.cn',
  #           'Referer': 'http://www.cninfo.com.cn/information/stock/financialreport_.jsp?stockCode=600600&key=0.9268299092833572',
  #           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
  #           'X-CSRF-Token': 'DfeIz+CdfLWv86lTgKmBu5xDl+hpbIxoE8wmxWIuhzECfwvWfO62+uO2dtqXaKh4nzSM4xRh3/TsTKrEbw73/Q=='
  #       }
		# yield scrapy.FormRequest(
		# 	self.base_url,
		# 	headers=headers,
		# 	formdata = {
		# 		'yyyy':'2017',
		# 		'mm':'-12-31',
		# 		'cwzb':'financialreport',
		# 		'button2':'提交'
		# 	},
		# 	callback = self.parse
		# )

	def parse(self,response):
		content = response.text
		soup = BeautifulSoup(content)
		content = soup.select('#cninfoform table tr td')
		print(content)
		pass
		# content = response.text
		# soup = BeautifulSoup(content)
		# content = soup.select('.clear table')
		# content = soup.select('tr')
		# content = soup.select('td')
		# # content = soup.select('div')
		# for elem in content:
		# 	# pass
		# 	print(elem)
# 0.28624108648063995
