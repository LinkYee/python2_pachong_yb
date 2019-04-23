#!/bin/python
#coding:utf8

from stock.items.items import CompanyItem

from stock.model.company import CompanyModel

class CompanyPipeline(object):
	"""把获取的股票保存到数据库里"""
	def process_item(self,item,spider):
		# print(item)
		company = CompanyModel.getInstance()
		if company.isExist(item['code']):
			company.insert(item)
		else:
			company.update(item)