#!/bin/python
# coding:utf8

from stock.items.items import LegalItem
from stock.model.notices import NoticesModel
from stock.model.noticeshk import NoticesHkModel
from stock.model.noticesns import NoticesNSModel


class NoticesPipeline(object):
    """把获取的公告保存到数据库"""

    def process_item(self, item, spider):

        if item['category'] == 1:
            notices = NoticesModel.getInstance()
            if notices.isExist(item['sid'],item['secu_code']):
                notices.insert(item)
        elif item['category'] == 2:
            notices = NoticesHkModel.getInstance()
            if notices.isExist(item['sid'], item['secu_code']):
                notices.insert(item)

        elif item['category'] == 3:
            notices = NoticesNSModel.getInstance()
            if notices.isExist(item['sid'], item['secu_code']):
                notices.insert(item)