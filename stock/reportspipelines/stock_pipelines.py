#!/bin/python
#coding:utf8

from stock.items.items import StockNewItem

from stock.model.stock import Stock

class StockPipeline(object):
	"""把获取的股票保存到数据库里"""
	def process_item(self,item,spider):
		stock = Stock.getInstance()

		if stock.isExist(item['code']):
			stock.insert(item)