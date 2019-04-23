#!/bin/python
# -*- coding: UTF-8 -*-
import scrapy
from scrapy.http import Request
from stock.items.items import NewsItem
from stock.model.stock import Stock
from bs4 import BeautifulSoup
import json
import time

# 公司详情爬虫
class News(scrapy.Spider):
	custom_settings = {
	    'ITEM_PIPELINES': {
		     'stock.reportspipelines.news_pipelines.NewsPipeline': 1,
		}
 	}
	name = 'news'
	base_url = "http://emweb.securities.eastmoney.com/PC_HSF10/NewsBulletin/NewsBulletinAjax?code=%s"
	content_url = 'http://stock.eastmoney.com/news/1699,%s.html'
	def start_requests(self):

		# code = self.getExchangeUrl('600600')
		# if code:
		# 	code = self.getExchange('600600')
		# 	yield Request(self.base_url % code,self.parse,meta={'code':code})

		stock = Stock.getInstance()
		page = 0
		while True:
			page += 1
			exchnage = stock.getStockInfo(page)
			if exchnage:
				for elem in exchnage:
					code = self.getExchangeUrl(elem[1])
					if code:
						sc_url = self.base_url % code
						code = self.getExchange(elem[1])
						yield Request(sc_url,self.parse,meta={'code':code})
			else:
				break

	def parse(self,response):
		code = response.meta['code']
		content = response.text
		json_data = json.loads(content)

		for elem in json_data['ggxx']['data']['items']:
			yield Request(self.content_url % elem['code'],callback=self.getContent,meta={'sid':elem['code'],'code':code})

	#获取内容
	def getContent(self,response):	
		soup = BeautifulSoup(response.text)

		title = soup.select('.newsContent h1')[0].string
		[s.extract() for s in soup('img')]

		sourch = soup.find('div',class_='data-source').attrs['data-source']
		content = soup.find('div',id='ContentBody').find_all('p')
		content = ''.join(str(s) for s in content)

		publ_date = soup.find('div',class_='time')
		publ_date = time.strptime(publ_date.string,u'%Y年%m月%d日 %H:%M')
		publ_date = time.strftime('%Y-%m-%d %H:%M:%S',publ_date)

		item = NewsItem()
		item['sid'] = response.meta['sid']
		item['secu_code'] = response.meta['code']
		item['title'] = title
		item['content'] = content
		item['url'] = response.url
		item['media'] = sourch
		item['publ_date'] = publ_date
		
		return item
	# 根据股票获取交易所
	def getExchange(self,code):
		first = int(code[0:1])
		if first == 6:
			return code+'.SS'
		elif first == 0 or first == 3:
			return code+'SZ'
		else:
			return None
	# 根据股票获取交易所
	def getExchangeUrl(self,code):
		first = int(code[0:1])
		if first == 6:
			return 'SH'+code
		elif first == 0 or first == 3:
			return 'SZ'+code
		else:
			return None