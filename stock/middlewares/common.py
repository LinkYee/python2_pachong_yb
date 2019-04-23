# -*- coding: UTF-8 -*-
from stock.model.error import ErrorLogModel
from stock.model.redis_model import RedisModel
import random
import time


class ErrorLog(object):
    """docstring for 错误日志"""

    @staticmethod
    def saveError(name, content):
        errorLog = ErrorLogModel.getInstance()
        errorLog.insert(name, content)


class RandomUserAgent(object):
    """
    动态设置 user agent
    """

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):

        request.headers.setdefault('User-Agent', random.choice(self.agents))


class ProxyMiddleWare(object):
    """动态获取"""

    def process_request(self, request, spider):
        '''对request对象加上proxy'''

        proxy = self.get_random_proxy()

        if len(proxy) != 0 and len(proxy) > 30:
            request.meta['proxy'] = proxy

    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            if request.url != 'http://api.ip.data5u.com/dynamic/get.html?order=94c34a04d262aa1fbee382841d2e97cf':
                proxy = self.get_random_proxy()

                request.meta['proxy'] = proxy
                time.sleep(40)
                return request
        return response

    def get_random_proxy(self):
        '''随机读取proxy'''

        redisModel = RedisModel()
        repeat = 0
        while True:
            ip_key = "ip_key_" + str(random.randint(0,6))
            proxy = redisModel.getName(ip_key)
            if proxy or repeat >= 2:
                break
            else:
                repeat += 1
        return str(proxy)
