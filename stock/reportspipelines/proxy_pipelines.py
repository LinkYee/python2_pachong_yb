#!/bin/python
#coding:utf8

from stock.model.redis_model import RedisModel

class ProxyPipeline(object):
	"""ip 存储在redis 里面"""


	def process_item(self,item,spider):
		
		redisModel = RedisModel()
		redisModel.setName('ip',item['ip'].strip('\n'),40)