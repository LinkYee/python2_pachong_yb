#!/bin/python
#coding:utf8
from connect import Connect
import time

class ErrorLogModel(Connect):
	"""连接数据库,记录爬虫错误日志"""
	table = 'mv_error_log' 
	instance = None
	def __init__(self):
		Connect.__init__(self)

	# 单例模式
	@classmethod
	def getInstance(cls):
		if not cls.instance:
			cls.instance = ErrorLogModel()
		return cls.instance

	# 插入数据库
	def insert(self,name,content):
		timeData = str(int(time.time()))

		sql = "insert into "+self.table+"(name,content,create_time,update_time) values(%s,%s,%s,%s)";
		data = (name,content,timeData,timeData)

		try:
			self.cur.execute(sql, data)
			self.con.commit()
		except Exception,e:
			print(e)
			self.con.rollback()
