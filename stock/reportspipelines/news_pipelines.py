#!/bin/python
#coding:utf8

from stock.items.items import NewsItem

from stock.model.news import NewsModel

class NewsPipeline(object):
	"""把获取的股票新闻保存到数据库里"""
	def process_item(self,item,spider):
		news = NewsModel.getInstance()
		if news.isExist(item['sid'],item['secu_code']):
			news.insert(item)
