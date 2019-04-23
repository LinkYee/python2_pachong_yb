# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from scrapy.http import HtmlResponse
import time


class NoticesMiddlewares(object):
    """docstring  巨潮财务信息"""

    def process_request(self, request, spider):
        if request.url.endswith('szse'):
            # print(request.url)
            # driver = webdriver.PhantomJS()
            # driver = webdriver.Chrome()
            # driver.maximize_window()

            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.get(request.url)
            # body = driver.page_source
            # input_first  = driver.find_element_by_id('stockID_')

            # input_first.clear()
            driver.implicitly_wait(3)
            # input_stock  = driver.find_element_by_css_selector('.drop-down-title')

            # ActionChains(driver).move_to_element(input_stock).perform()
            # menu = driver.find_element_by_xpath('//*[@id="plate_list"]')
            # menu
            # time.sleep(10).click()
            # time.sleep(10)

            driver.find_element_by_css_selector('.com-search-btn').click()
            # btn  = driver.find_element_by_css_selector('#ul_a_latest .t1')
            # btn.click()
            # print(btn)


            # btn = driver.find_element_by_xpath("//div[@class='com-search-btn']")
            # print(btn)
            # btn.click()
            # driver.execute_script(js)
            # input_stock  = driver.find_element_by_css_selector('.search-condition')
            # WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.ID, "his_fulltext"))
            # ActionChains(driver).move_to_element(input_stock).perform()
            # btn  = driver.find_element_by_css_selector('.com-search-btn')
            # btn.click()
            driver.implicitly_wait(3)
            # time.sleep(15)
            # print(body)
            # print(driver.get_cookies())
            # cookie={}
            # for i in driver.get_cookies():
            # 	print(i)
            # 	cookie[i["name"]] = i["value"]

            # print(cookie)
            # wait = WebDriverWait(driver, 1)
            # input = wait.until(EC.presence_of_element_located((By.ID, 'q')))
            # input_first.send_keys('000150')
            # driver.execute_script('window.open("https://www.v2ex.com")')
            handles = driver.window_handles
            driver.switch_to_window(handles[1])
            driver.find_element_by_css_selector('.com-search-btn').click()
            print(handles)
            # driver.switch_to_window(driver.window_handles[1])

            body = driver.page_source

            # time.sleep(10)
            # title = driver.find_element_by_id('title')
            # print(By.ID)
            # title.clear()
            # dataClick = button.click()
            # print(dataClick)
            # body = driver.page_source
            # # driver.switch_to.frame('i_nr')
            # # print("访问：", driver.page_source)
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8')


    def process_response(self, request, response, spider):
        if response.status != 200:

            return request
        else:
            return response
