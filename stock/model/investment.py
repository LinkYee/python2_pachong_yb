#!/bin/python
# coding:utf8
from connect import Connect
import time


class InvestmentAskModel(Connect):
    """连接数据库"""
    table = 'mv_investment_ask'
    instance = None

    def __init__(self):
        Connect.__init__(self)

    # 单例模式
    @classmethod
    def getInstance(cls):
        if not cls.instance:
            cls.instance = InvestmentAskModel()
        return cls.instance

    # 数据是否存在
    def isExist(self, sid):
        sql = "select count(*) from %s where sid='%s'" % (self.table, sid);
        self.cur.execute(sql)
        res = self.cur.fetchone()
        if res[0] > 0:
            return False
        else:
            return True

    # 数据信息
    def getId(self, sid):
        sql = "select id from %s where sid='%s'" % (self.table, sid);
        self.cur.execute(sql)
        res = self.cur.fetchone()
        return res[0]

    # 插入数据库
    def insert(self, param):
        timeData = str(int(time.time()))
        sql = "insert into " + self.table + "(sid,name,category,title,content,pdate,reply_num,create_time) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        data = (
            param['sid'], param['name'], param['category'], param['title'], param['content'], param['pdate'],
            param['reply_num'], timeData)

        try:
            self.cur.execute(sql, data)
            self.con.commit()
        except Exception as e:
            print(e)
            print(param['sid'])
            self.con.rollback()

    # 更新数据库
    def update(self, param):
        timeData = str(int(time.time()))

    # sql = "update "+self.table+" set profile =%s,manager = %s,theme=%s,update_time=%s where code = %s";
    # data = (param['profile'],param['manager'],param['theme'],timeData,param['code'])

    # try:
    # 	self.cur.execute(sql, data)
    # 	self.con.commit()
    # except Exception,e:
    # 	self.con.rollback()


class InvestmentReplyModel(Connect):
    """连接数据库"""
    table = 'mv_investment_reply'
    instance = None

    def __init__(self):
        Connect.__init__(self)

    # 单例模式
    @classmethod
    def getInstance(cls):
        if not cls.instance:
            cls.instance = InvestmentReplyModel()
        return cls.instance

    # 数据是否存在
    def isExist(self, sid):
        sql = "select count(*) from %s where sid='%s'" % (self.table, sid)
        self.cur.execute(sql)
        res = self.cur.fetchone()
        if res[0] > 0:
            return False
        else:
            return True

    # 插入数据库
    def insert(self, param):
        timeData = str(int(time.time()))

        sql = "insert into " + self.table + "(sid,ask_id, name,content,pdate,best,create_time) values(%s,%s,%s,%s,%s,%s,%s)"
        data = (param['sid'], param['ask_id'], param['name'], param['content'], param['pdate'], param['best'], timeData)

        try:
            self.cur.execute(sql, data)
            self.con.commit()
        except Exception as e:
            print(e)
            print param['sid']
            self.con.rollback()
