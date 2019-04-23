#!/bin/python
# -*- coding: UTF-8 -*-
import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from stock.items.items import ReportsHyItem
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
	name = 'reports_industry'
	bash_url = 'http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=HYSR&mkt=0&stat=0&cmd=4&code=&sc=&ps=50&p=%d&js=var OjmxomUw={"data":[(x)],"pages":"(pc)","update":"(ud)","count":"(count)"}&rt=51210030'

	# pageTotal = 2
	def start_requests(self):
		for page in xrange(1,3):
			sc_url = self.bash_url % page
			yield Request(sc_url, callback=self.parse)
		# yield Request(self.bash_url % '000656',self.parse)
		# stock = Stock.getInstance()
		# page = 0
		# while True:
		# 	page += 1
		#
		# 	if self.pageTotal != -1 and page > self.pageTotal:
		# 		break
		# 	else:
		# 		sc_url = self.bash_url % page
		# 		yield Request(sc_url, callback=self.parse)
				# break


	def parse(self,response):
		try:
			content = response.body_as_unicode()
			content = json.loads(content[13:])

			# if self.pageTotal == -1:
			# 	self.pageTotal = content['pages']

			for elem in content['data']:
				data = elem.split(',')

				publ_date = time.strptime(data[1],'%Y/%m/%d %H:%M:%S')
				datetime = time.strftime('%Y%m%d',publ_date)

				# 只同步当天的研报，提高性能
				# if datetime != time.strftime('%Y%m%d'):
				# 	continue

				content_url = 'http://data.eastmoney.com/report/%s/hy,%s.html' % (datetime,data[2])
				meta = {
					'title':data[9],
					'name':data[10],
					'sid':data[2],
					'invest_statement':data[0],
					'org_name':data[4],
					'pdate':time.strftime('%Y-%m-%d',publ_date)
				}

				yield Request(content_url,callback=self.getContent,meta=meta)
				# yield Request(content_url,callback=self.getContent)
		except Exception as e:
			print(e)

	
	# 获取内容数据	
	def getContent(self,response):
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




