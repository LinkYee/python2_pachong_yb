#!/bin/python
#coding:utf8

from stock.model.investment import InvestmentAskModel, InvestmentReplyModel


class InvestmentPipeline(object):
	"""把获取的法规保存到数据库里"""


	def process_item(self,item,spider):

		if item['type'] == 0:
			investment = InvestmentAskModel.getInstance()
			if investment.isExist(item['sid']):
				investment.insert(item)
		else:
			investmentAsk = InvestmentAskModel.getInstance()

			item['ask_id'] = investmentAsk.getId(item['sid'])

			investment = InvestmentReplyModel.getInstance()
			investment.insert(item)