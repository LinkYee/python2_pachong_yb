# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StockItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()


# 研报数据
class ReportsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sid = scrapy.Field()
    secu_code = scrapy.Field()
    title = scrapy.Field()
    conclusion = scrapy.Field()
    org_name = scrapy.Field()
    invest_statement = scrapy.Field()
    url = scrapy.Field()
    publ_date = scrapy.Field()


# 研报数据
class ReportsHyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sid = scrapy.Field()
    name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    org_name = scrapy.Field()
    invest_statement = scrapy.Field()
    url = scrapy.Field()
    pdate = scrapy.Field()


# 研报微信数据
class ReportsWxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sid = scrapy.Field()
    name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    org_name = scrapy.Field()
    invest_statement = scrapy.Field()
    url = scrapy.Field()
    pdate = scrapy.Field()
    type = scrapy.Field()

# 机构研报数据
class ReportsOrgItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sid = scrapy.Field()
    name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    org_name = scrapy.Field()
    label_name = scrapy.Field()
    invest_statement = scrapy.Field()
    url = scrapy.Field()
    pdate = scrapy.Field()


# 股票数据
class StockNewItem(scrapy.Item):
    code = scrapy.Field()
    name = scrapy.Field()
    exchange = scrapy.Field()


# 公司详情
class CompanyItem(scrapy.Item):
    code = scrapy.Field()
    profile = scrapy.Field()
    manager = scrapy.Field()
    theme = scrapy.Field()


# 新闻详情
class NewsItem(scrapy.Item):
    sid = scrapy.Field()
    secu_code = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    media = scrapy.Field()
    publ_date = scrapy.Field()


# 法律法规
class LegalItem(scrapy.Item):
    sid = scrapy.Field()
    title = scrapy.Field()
    mold = scrapy.Field()
    catalog = scrapy.Field()
    content = scrapy.Field()
    pdate = scrapy.Field()
    status = scrapy.Field()
    enact = scrapy.Field()
    category = scrapy.Field()
    attachment = scrapy.Field()


# 颁布机构
class EnactItem(scrapy.Item):
    name = scrapy.Field()


# 颁布机构
class NoticesItem(scrapy.Item):
    sid = scrapy.Field()
    secu_code = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    category = scrapy.Field()


# 新三板法库
class NeeqItem(scrapy.Item):
    infoId = scrapy.Field()
    fileName = scrapy.Field()
    fileUrl = scrapy.Field()
    title = scrapy.Field()
    pdate = scrapy.Field()
    category = scrapy.Field()
    content = scrapy.Field()

# 投行先锋问答
class InvestmentItem(scrapy.Item):
    ask_id = scrapy.Field()
    sid = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    pdate = scrapy.Field()
    reply_num = scrapy.Field()
    best = scrapy.Field()
    type = scrapy.Field()
# 投行先锋问答
class ProxyIpItem(scrapy.Item):
    ip = scrapy.Field()

# 法规案例
class LegalCaseItem(scrapy.Item):
    sid = scrapy.Field()
    category = scrapy.Field()
    title = scrapy.Field()
    org_name = scrapy.Field()
    pdate = scrapy.Field()
    reference_num = scrapy.Field()
    content = scrapy.Field()




