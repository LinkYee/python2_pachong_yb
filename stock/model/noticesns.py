#!/bin/python
# coding:utf8
from connect import Connect
import time


class NoticesNSModel(Connect):
    """连接数据库"""
    table = 'mv_stock_noticesns'
    instance = None

    def __init__(self):
        Connect.__init__(self)


    # 单例模式
    @classmethod
    def getInstance(cls):
        if not cls.instance:
            cls.instance = NoticesNSModel()
        return cls.instance

    #是否存在
    def isExist(self, sid, code):
        sql = "select count(*) from "+self.table+" where sid='%s' and secu_code = '%s'" % (sid, code)
        self.cur.execute(sql)
        res = self.cur.fetchone()
        if res[0] > 0:
            return False
        else:
            return True
    # 新增数据
    def insert(self, param):
        timeData = int(time.time())

        sql = "insert into "+ self.table +"(sid,secu_code,title,url,date,create_time,update_time) values('%s','%s','%s','%s','%s',%d,%d)" % (
        param['sid'], param['secu_code'], param['title'], param['url'], param['date'], timeData, timeData);
        try:
            self.cur.execute(sql)
            # print(self.cur.lastrowid)
            self.con.commit()
        except Exception as e:
            self.con.rollback()
            print(e)


