# -*- coding: utf-8 -*-
import scrapy
import json
from stock.items.items import NeeqItem
import time
# 新三板法规 http://www.neeq.com.cn
class Neeq(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES': {
            # 'scrapy.pipeline.files.FilesPipeline': 1,
            'stock.reportspipelines.neeq_pipelines.NeeqPipeline': 10
        },
        'FILES_STORE' : 'examples_src'
    }
    name = 'neeq'
    base_url = 'http://www.neeq.com.cn/info/node_list.do?callback=jQuery'
    local = 'http://www.neeq.com.cn'
    def start_requests(self):
        headers = {
            "Host":"www.neeq.com.cn",
            "Referer":"http://www.neeq.com.cn/rule/Business_rules.html",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        yield scrapy.FormRequest(
            self.base_url,
            formdata={
                'nodeId': '107',
                'keywords':''
            },
            headers = headers,
            callback=self.parse
        )
    def parse(self, response):
        content = response.text
        content = json.loads(content[7:-1])
        # print(content[0]['data'])
        for elem in content[0]['data']:

            for e in elem['info']:
                item = NeeqItem()
                item['category'] = elem['nodeName']
                item['infoId'] = e['infoId']
                item['fileName'] = e['fileName']
                item['fileUrl'] = (self.local + e['fileUrl'] if e['fileUrl'] != '' else '')
                item['title'] = e['title']
                publ_date = time.strptime(e['publishDate'][:-2], '%Y-%m-%d %H:%M:%S')
                datetime = time.strftime('%Y-%m-%d', publ_date)
                item['pdate'] = datetime
                item['content'] = e['text']
                yield item
