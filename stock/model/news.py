#!/bin/python
#coding:utf8
from connect import Connect
import time

class NewsModel(Connect):
	"""连接数据库"""
	table = 'mv_stock_news' 
	instance = None
	def __init__(self):
		Connect.__init__(self)

	# 单例模式
	@classmethod
	def getInstance(cls):
		if not cls.instance:
			cls.instance = NewsModel()
		return cls.instance

	# 数据是否存在
	def isExist (self,sid,code):
		sql = "select count(*) from %s where sid = '%s' and secu_code='%s'" % (self.table,sid,code);
		self.cur.execute(sql)
		res = self.cur.fetchone()

		if res[0] > 0:
			return False
		else:
			return True
	# 插入数据库
	def insert(self,param):
		timeData = str(int(time.time()))
		
		sql = "insert into "+self.table+"(sid,secu_code,title,content,url,media,publ_date,create_time,update_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)";
		data = (param['sid'],param['secu_code'],param['title'],param['content'],param['url'],param['media'],param['publ_date'],timeData,timeData)

		try:
			self.cur.execute(sql, data)
			self.con.commit()
		except Exception,e:
			print(e)
			self.con.rollback()