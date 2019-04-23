# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
import time
class LegalMiddlewares(object):
	"""docstring  巨潮财务信息"""
	def process_request(self, request, spider):
		
		if request.url.endswith('.html'):
			# print(request.url)
			driver = webdriver.PhantomJS()
			# driver = webdriver.Chrome()
			driver.get(request.url)
			body = driver.page_source
			# input_first  = driver.find_element_by_id('stockID_')
			# input_first.clear()
			driver.implicitly_wait(20)
			# wait = WebDriverWait(driver, 20)
			# input = wait.until(EC.visibility_of_element_located((By.ID, 'itemList')))
			# input_first.send_keys('000150')
			# time.sleep(10)


			# print(By.ID)
			# title.clear()
			# dataClick = button.click()
			# print(dataClick)
			# body = driver.page_source
			# # driver.switch_to.frame('i_nr')
			# # print("访问：", driver.page_source)
			return HtmlResponse(driver.current_url, body=body, encoding='utf-8')

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
		 

		