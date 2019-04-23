#!/bin/python
#coding:utf8

from connect import Connect
import time
class Stock(Connect):
	"""连接数据库"""
	table = 'mv_stock' 
	instance = None
	def __init__(self):
		Connect.__init__(self)

	# 单例模式
	@classmethod
	def  getInstance(cls):
		if not cls.instance:
			cls.instance = Stock()
		return cls.instance

	# 获取code对应的交易所的值
	def getExchange(self,code):
		sql = "select id,code,exchange from %s where code='%s'" % (Stock.table,code);
		self.cur.execute(sql)
		res = self.cur.fetchone()
		if res:
			if res[2] == 'SS.ESA':
				return code+'.SS'
			elif res[2] == 'SZ.ESA':
				return code+'.SZ'
			else:
				return ''
	#获取股票数
	def getStockInfo(self,page):
			start = (page-1)*10
			sql = "select id,code from %s where exchange in('SS.ESA','SZ.ESA') limit %d,10" % (Stock.table,start)
			self.cur.execute(sql)

			return self.cur.fetchall()
	# 股票是否存在
	def isExist (self,code):
		sql = "select count(*) from %s where code ='%s'" % (self.table,code);

		self.cur.execute(sql)
		res = self.cur.fetchone()
		if res[0] > 0:
			return False
		else:
			return True
	# 插入数据库
	def insert(self,param):
		timeData = str(int(time.time()))

		sql = "insert into "+self.table+"(code,`name`,exchange,create_time,update_time) values(%s,%s,%s,%s,%s)";
		data = (param['code'],param['name'],param['exchange'],timeData,timeData)

		try:
			self.cur.execute(sql, data)
			self.con.commit()
		except Exception as e:

			self.con.rollback()