#!/bin/python
#coding:utf8
from connect import Connect
import time

class CompanyModel(Connect):
	"""连接数据库"""
	table = 'mv_stock_company' 
	instance = None
	def __init__(self):
		Connect.__init__(self)

	# 单例模式
	@classmethod
	def getInstance(cls):
		if not cls.instance:
			cls.instance = CompanyModel()
		return cls.instance

	# 数据是否存在
	def isExist (self,code):
		sql = "select count(*) from %s where code='%s'" % (self.table,code);
		self.cur.execute(sql)
		res = self.cur.fetchone()
		if res[0] > 0:
			return False
		else:
			return True
	# 插入数据库
	def insert(self,param):
		timeData = str(int(time.time()))
		
		if 'profile' not in param:
			param['profile'] = ''
		if 'manager' not in param:
			param['manager'] = ''
		if 'theme' not in param:
			param['theme'] = ''


		sql = "insert into "+self.table+"(code,profile,manager,theme,create_time,update_time) values(%s,%s,%s,%s,%s,%s)";
		data = (param['code'],param['profile'],param['manager'],param['theme'],timeData,timeData)

		try:
			self.cur.execute(sql, data)
			self.con.commit()
		except Exception,e:
			self.con.rollback()
	# 更新数据库
	def update(self,param):
		timeData = str(int(time.time()))

		sql = "update "+self.table+" set profile =%s,manager = %s,theme=%s,update_time=%s where code = %s";
		data = (param['profile'],param['manager'],param['theme'],timeData,param['code'])

		try:
			self.cur.execute(sql, data)
			self.con.commit()
		except Exception,e:
			self.con.rollback()