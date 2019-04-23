#!/bin/python
#coding:utf8
from connect import Connect
import time

class EnactModel(Connect):
	"""法律颁布机构"""
	table = 'mv_legal_enact' 
	instance = None
	def __init__(self):
		Connect.__init__(self)

	# 单例模式
	@classmethod
	def getInstance(cls):
		if not cls.instance:
			cls.instance = EnactModel()
		return cls.instance

	# 数据是否存在
	def isExist (self,name):
		sql = "select count(*) from %s where name='%s'" % (self.table,name);
		self.cur.execute(sql)
		res = self.cur.fetchone()
		if res[0] > 0:
			return False
		else:
			return True
	# 插入数据库
	def insert(self,name):
		timeData = str(int(time.time()))


		sql = "insert into "+self.table+"(name,create_time) values(%s,%s)";
		data = (name,timeData)

		try:
			self.cur.execute(sql, data)
			self.con.commit()
		except Exception,e:
			print e
			self.con.rollback()
	# 获取机构名称
	def getEnactInfo(self,name):

		sql = "select * from %s where name='%s'" % (self.table,name)
		self.cur.execute(sql)

		return self.cur.fetchone()
