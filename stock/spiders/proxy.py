#!/bin/python
# -*- coding: UTF-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
from stock.items.items import ProxyIpItem
import time

# 公司详情爬虫
class Proxyy(scrapy.Spider):
	'''
	动态获取ip
	'''
	custom_settings = {
	    'ITEM_PIPELINES': {
		     'stock.reportspipelines.proxy_pipelines.ProxyPipeline': 100,
		}
 	}
	# custom_settings = None
	name = 'proxy_ip'
	base_url = "http://api.ip.data5u.com/dynamic/get.html?order=94c34a04d262aa1fbee382841d2e97cf"

	# @classmethod
	# def update_settings(cls, settings):
	# 	sett = get_project_settings()
	# 	item = settings.get('DOWNLOADER_MIDDLEWARES')
	# 	custom_settings = {
	# 		'ITEM_PIPELINES': {
	# 			'stock.reportspipelines.proxy_pipelines.ProxyPipeline': 100,
	# 		},
	# 		'DOWNLOADER_MIDDLEWARES': {
	# 			'stock.middlewares.legal.LegalMiddlewares': 1,
	# 		}
	# 	}
	# 	for k, v in item.items():
	# 		custom_settings['DOWNLOADER_MIDDLEWARES'][k] = v
	# 	cls.custom_settings = custom_settings
	#
	# 	settings.setdict(cls.custom_settings or {}, priority='spider')

	def start_requests(self):
		yield Request(self.base_url, self.parse)
	# 解析公司概要
	def parse(self,response):

		content = response.text
		item = ProxyIpItem()
		item['ip'] = content
		yield  item

