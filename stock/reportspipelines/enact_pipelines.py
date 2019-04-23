#!/bin/python
#coding:utf8

from stock.model.enact import EnactModel

class EnactPipeline(object):
	"""把获取的机构保存到数据库"""

	def process_item(self,item,spider):
		enact = EnactModel.getInstance()
		# print(enact.isExist(item['name']))
		if enact.isExist(item['name']):
			enact.insert(item['name'])