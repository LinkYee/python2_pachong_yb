#!/bin/python
#coding:utf8

from stock.items.items import LegalItem
from stock.model.legal import LegalModel, LegalCaseModel

class LegalPipeline(object):
	"""把获取的法规保存到数据库里"""


	def process_item(self,item,spider):
		
		legal = LegalModel.getInstance()

		if legal.isExist(item['sid']):
			legal.insert(item)



class LegalCasePipeline(object):
	'''
	法律案例保存到数据库
	'''
	def process_item(self,item,spider):
		legalCase = LegalCaseModel.getInstance()
		if legalCase.isExist(item['sid']):
			legalCase.insert(item)