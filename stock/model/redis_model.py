#!/bin/python
# coding:utf8
import redis


class RedisModel(object):
    """连接redis"""
    instance = None
    def __init__(self):
        self.conn = redis.Redis(
            host='106.14.179.226',
            port=6379,
            password='Szb!20181109',
            decode_responses=True)

    # 单例模式
    @classmethod
    def getInstance(cls):
        if not cls.instance:
            cls.instance = RedisModel()
        return cls.instance

    # 关闭redis连接
    def close(self):
        self.close();

    # 获取值
    def getName(self, name):
        return self.conn.get(name)

    # 设置值
    def setName(self, name, value, ex=None):
        return self.conn.set(name, value, ex)

    # 从集合右侧中移除一个元素
    def spop(self, name):
        return self.conn.spop(name)

    def sadd(self, name, item):
        '''
        向集合中添加一个元素
        :param name:
        :param item:
        :return:
        '''
        return self.conn.sadd(name, item)
