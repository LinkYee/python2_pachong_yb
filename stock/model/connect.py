#!/usr/bin/python
#coding:utf-8
from scrapy.utils.project import get_project_settings
import MySQLdb

settings = get_project_settings()

MYSQL_HOSTS = settings.get('MYSQL_HOSTS')
MYSQL_USER  = settings.get('MYSQL_USER')
MYSQL_PASSWORD = settings.get('MYSQL_PASSWORD')
MYSQL_DB = settings.get('MYSQL_DB')

class Connect(object):
	"""连接数据库"""
	def __init__(self):
		self.con = MySQLdb.connect(MYSQL_HOSTS,MYSQL_USER,MYSQL_PASSWORD,MYSQL_DB);
		self.con.set_character_set('utf8')
		self.cur = self.con.cursor();
		self.cur.execute("SET NAMES utf8")

	# 关闭数据库连接
	def close(self):
		self.con.close()
		