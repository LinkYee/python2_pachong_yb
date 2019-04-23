# -*- coding: utf-8 -*-
from selenium import webdriver
from scrapy.http import HtmlResponse
import time
class FinanceMiddlewares(object):
	"""docstring  巨潮财务信息"""
	def process_request(self, request, spider):
		driver = webdriver.PhantomJS()
		# driver = webdriver.Chrome()
		driver.get(request.url)
		body = driver.page_source
		input_first  = driver.find_element_by_id('stockID_')
		input_first.clear()

		input_first.send_keys('000150')

		button = driver.find_element_by_id('button')
		dataClick = button.click()
		print(dataClick)
		body = driver.page_source
		# driver.switch_to.frame('i_nr')
		# print("访问：", driver.page_source)
		return HtmlResponse(driver.current_url, body=body, encoding='utf-8')

		