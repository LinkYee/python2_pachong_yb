# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from stock.model.redis_model import RedisModel
import time
import json


class ReportsWxMiddlewares(object):
    """docstring  微信公众号请求处理"""

    def process_request(self, request, spider):
        if request.url == 'https://mp.weixin.qq.com/':
            post = {}
            # driver = webdriver.PhantomJS()
            driver = webdriver.Chrome()
            driver.get(request.url)
            # time.sleep(2)
            driver.find_element_by_xpath("./*//input[@name='account']").clear()
            driver.find_element_by_xpath("./*//input[@name='account']").send_keys('775685514@qq.com')
            # 清空密码框中的内容
            driver.find_element_by_xpath("./*//input[@name='password']").clear()
            # 自动填入登录密码
            driver.find_element_by_xpath("./*//input[@name='password']").send_keys('wmt775685514')
            # 登录
            driver.find_element_by_xpath("./*//a[@class='btn_login']").click()
            time.sleep(10)
            driver.get(request.url)
            cookie_items = driver.get_cookies()
            body = driver.page_source
            for cookie_item in cookie_items:
                post[cookie_item['name']] = cookie_item['value']
            cookie_str = json.dumps(post)

            RedisModel.getInstance().setName('wx_cookie', cookie_str, 3600)
            # time.sleep(10)
            return HtmlResponse(driver.current_url, encoding='utf-8')
        request.cookies = self.get_random_cookies()
        return None

    def process_response(self, request, response, spider):
        # print(response.status)
        return response

    # 如果返回的response状态不是200，重新生成当前request对象

    # if response.status != 200:
    # proxy = self.get_random_proxy()
    # print("this is response ip:"+proxy)
    # # 对当前reque加上代理
    # request.meta['proxy'] = proxy
    # return request

    def get_random_cookies(self):
        wx_cookie = RedisModel.getInstance().getName('wx_cookie')
        if wx_cookie:
            return json.loads(wx_cookie)


class ReportsWxSogouMiddlewares(object):
    """docstring  微信公众号请求处理 前10条数据"""

    def process_request(self, request, spider):
        if request.url.find('mp.weixin.qq.com') != -1:
            post = {}
            # driver = webdriver.PhantomJS()
            driver = webdriver.Chrome()
            driver.get(request.url)

            body = driver.page_source
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8')
        return None

    def process_response(self, request, response, spider):
        # print(response.status)
        return response
