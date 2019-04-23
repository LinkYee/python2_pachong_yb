#!/bin/python
# coding:utf8

import scrapy
from scrapy.pipelines.files import FilesPipeline
from urlparse import urlparse
from os.path import basename, dirname, join

from stock.model.legal import LegalNeeqModel


class NeeqPipeline(FilesPipeline):
    """把获取的新三板下载"""

    # def process_item(self, item, spider):
    #     print(333)

    # legal = LegalModel.getInstance()
    #
    # if legal.isExist(item['sid']):
    # 	legal.insert(item)

    def get_media_requests(self, item, info):
        legalNeeq = LegalNeeqModel.getInstance()
        if legalNeeq.isExist(item['infoId']):
            legalNeeq.insert(item)
            if item['fileUrl']:
                yield scrapy.Request(item['fileUrl'], meta={'fileName': item['fileName']})

    def file_path(self, request, response=None, info=None):
        path = urlparse(request.url).path

        return join(basename(dirname(path)), basename(request.meta['fileName']))
