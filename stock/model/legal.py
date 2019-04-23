#!/bin/python
# coding:utf8
from connect import Connect
import time


class LegalModel(Connect):
    """连接数据库"""
    table = 'mv_legal'
    instance = None

    def __init__(self):
        Connect.__init__(self)

    # 单例模式
    @classmethod
    def getInstance(cls):
        if not cls.instance:
            cls.instance = LegalModel()
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

    # 插入数据库
    def insert(self, param):
        timeData = str(int(time.time()))
        create_time = time.strftime('%Y-%m-%d %H:%M:%S')

        sql = "insert into " + self.table + "(sid,title,mold,enact,category,catalog,content,pdate,status,attachment,create_time,update_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
        data = (param['sid'], param['title'], param['mold'], param['enact'], param['category'], param['catalog'],
                param['content'], param['pdate'], param['status'], param['attachment'], create_time, timeData)

        try:
            self.cur.execute(sql, data)
            self.con.commit()
        except Exception, e:
            print(e)
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


class LegalNeeqModel(Connect):
    """连接数据库"""
    table = 'mv_legal_neeq'
    instance = None

    def __init__(self):
        Connect.__init__(self)

    # 单例模式
    @classmethod
    def getInstance(cls):
        if not cls.instance:
            cls.instance = LegalNeeqModel()
        return cls.instance

    # 数据是否存在
    def isExist(self, infoId):
        sql = "select count(*) from %s where info_id='%s'" % (self.table, infoId);
        self.cur.execute(sql)
        res = self.cur.fetchone()
        if res[0] > 0:
            return False
        else:
            return True

    # 插入数据库
    def insert(self, param):
        timeData = str(int(time.time()))

        sql = "insert into " + self.table + "(info_id,title,content,file_name,file_url,pdate,category,create_time) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        data = (param['infoId'], param['title'], param['content'], param['fileName'], param['fileUrl'], param['pdate'],
                param['category'], timeData)

        try:
            self.cur.execute(sql, data)
            self.con.commit()
        except Exception, e:
            print(e)
            self.con.rollback()


class LegalCaseModel(Connect):
    """连接数据库-法规案例"""
    table = 'mv_legal_case'
    instance = None

    def __init__(self):
        Connect.__init__(self)

    # 单例模式
    @classmethod
    def getInstance(cls):
        if not cls.instance:
            cls.instance = LegalCaseModel()
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

        sql = "insert into " + self.table + "(sid,title,content,category,org_name,pdate,reference_num,create_time) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        data = (param['sid'], param['title'], param['content'], param['category'], param['org_name'], param['pdate'],
                param['reference_num'], timeData)

        try:
            self.cur.execute(sql, data)
            self.con.commit()
        except Exception, e:
            print(e)
            self.con.rollback()
