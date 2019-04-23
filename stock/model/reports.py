#!/bin/python
# coding:utf8
from connect import Connect
import time


class Reports(Connect):
    """连接数据库"""
    table = 'mv_stock_reports'
    instance = None

    def __init__(self):
        Connect.__init__(self)

    # 单例模式
    @classmethod
    def getInstance(cls):
        if not cls.instance:
            cls.instance = Reports()
        return cls.instance

    # 插入数据库
    def insert(self, param):
        timeData = str(int(time.time()))

        sql = "insert into " + self.table + "(sid,secu_code,title,conclusion,invest_statement,org_name,url,publ_date,create_time,update_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
        data = (param['sid'], param['secu_code'], param['title'], param['conclusion'], param['invest_statement'],
                param['org_name'], param['url'], param['publ_date'], timeData, timeData)

        try:
            self.cur.execute(sql, data)
            self.con.commit()
        except Exception as e:

            self.con.rollback()

    # 数据是否存在
    def isExist(self, sid, secu_code):
        sql = "select count(*) from %s where sid ='%s' and secu_code='%s'" % (self.table, sid, secu_code);
        self.cur.execute(sql)
        res = self.cur.fetchone()
        if res[0] > 0:
            return False
        else:
            return True


class ReportsHy(Connect):
    """连接数据库"""
    table = 'mv_reports_hy'
    instance = None

    def __init__(self):
        Connect.__init__(self)

    # 单例模式
    @classmethod
    def getInstance(cls):
        if not cls.instance:
            cls.instance = ReportsHy()
        return cls.instance

    # 插入数据库
    def insert(self, param):
        timeData = str(int(time.time()))

        sql = "insert into " + self.table + "(sid,name,title,content,invest_statement,org_name,url,pdate,create_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)";
        data = (
            param['sid'], param['name'], param['title'], param['content'], param['invest_statement'], param['org_name'],
            param['url'], param['pdate'], timeData)

        try:
            self.cur.execute(sql, data)
            self.con.commit()
        except Exception as e:

            self.con.rollback()

    # 数据是否存在
    def isExist(self, sid):
        sql = "select count(*) from %s where sid ='%s' " % (self.table, sid)
        self.cur.execute(sql)
        res = self.cur.fetchone()
        if res[0] > 0:
            return False
        else:
            return True


class ReportsOrg(Connect):
    """连接数据库"""
    table = 'mv_reports_org'
    instance = None

    def __init__(self):
        Connect.__init__(self)

    # 单例模式
    @classmethod
    def getInstance(cls):
        if not cls.instance:
            cls.instance = ReportsOrg()
        return cls.instance

    # 插入数据库
    def insert(self, param):
        timeData = str(int(time.time()))

        sql = "insert into " + self.table + "(sid,name,label_name,title,content,invest_statement,org_name,url,pdate,create_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
        data = (
            param['sid'], param['name'], param['label_name'], param['title'], param['content'],
            param['invest_statement'], param['org_name'],
            param['url'], param['pdate'], timeData)

        try:
            self.cur.execute(sql, data)
            self.con.commit()
        except Exception as e:

            self.con.rollback()

    # 数据是否存在
    def isExist(self, sid):
        sql = "select count(*) from %s where sid ='%s' " % (self.table, sid)
        self.cur.execute(sql)
        res = self.cur.fetchone()
        if res[0] > 0:
            return False
        else:
            return True


class ReportsWx(Connect):
    """数据库微信研报公告文章"""
    table = 'mv_reports_wx'
    instance = None

    def __init__(self):
        Connect.__init__(self)

    # 单例模式
    @classmethod
    def getInstance(cls):
        if not cls.instance:
            cls.instance = ReportsWx()
        return cls.instance

    # 插入数据库
    def insert(self, param):
        timeData = str(int(time.time()))

        sql = "insert into " + self.table + "(sid,title,content,org_name,pdate,create_time) values(%s,%s,%s,%s,%s,%s)";
        data = (
            param['sid'], param['title'], param['content'], param['org_name'],
            param['pdate'], timeData)

        try:
            self.cur.execute(sql, data)
            self.con.commit()
        except Exception as e:

            self.con.rollback()

    # 数据是否存在
    def isExist(self, sid):
        sql = "select count(*) from %s where sid ='%s' " % (self.table, sid)
        self.cur.execute(sql)
        res = self.cur.fetchone()
        if res[0] > 0:
            return False
        else:
            return True

