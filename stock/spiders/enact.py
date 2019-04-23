#!/bin/python
# -*- coding: UTF-8 -*-
import scrapy
from stock.items.items import EnactItem
from stock.middlewares.common import ErrorLog
import json


# 法律法规 颁布机构
# 爬取的数据地址：/laws/laws.html
class Finance(scrapy.Spider):

 	custom_settings = {
	    'ITEM_PIPELINES': {
		     'stock.reportspipelines.enact_pipelines.EnactPipeline': 1,
		}
		# ,
		# 'DOWNLOADER_MIDDLEWARES': {
		#      'stock.middlewares.legal.LegalMiddlewares': 1,
		# }
 	}
	name = 'enact'
	base_url = "http://www.valueonline.cn/laws/laws/lawsManage"

	def start_requests(self):
		for x in xrange(1,262):
			x = str(x)
			yield scrapy.FormRequest(
				self.base_url,
				formdata = {
					'id':'99',
					'pageNo':x,
					'pageSize':'20'
				},
				callback = self.parse,
				errback = self.error_handle
			)

	def parse(self,response):
		content = response.body_as_unicode()

		content = json.loads(content)
		for elem in content['result']['lawsManageList']:
			elemList = elem['lawSourceName'].split(',')
			for x in elemList:
				item = EnactItem()
				item['name'] = x
				yield item


	# 错误请求
	def error_handle (self,response):
		ErrorLog.saveError(self.name,response.value)


