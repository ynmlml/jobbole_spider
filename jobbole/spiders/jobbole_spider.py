# -*- coding: utf-8 -*-

import sys
type_ = sys.getfilesystemencoding()
reload(sys)
sys.setdefaultencoding('utf-8')

from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from jobbole.items import JobboleItem
from scrapy.selector import Selector

class Jobspider(Spider):
    page_link=set()#
    content_link=set()
    name='jobbole'
    allowed_domain=['jobbole.com']
    start_urls=['http://python.jobbole.com/all-posts/']
    rules={'page':LinkExtractor(allow=('http://python.jobbole.com/all-posts/page/\d+/')),
         'content':LinkExtractor(allow=('http://python.jobbole.com/\d+/'))}

    #start_urls的网址会第一个传到parse()
    def parse(self,response):
        for link in self.rules['page'].extract_links(response):
        #对于找到的每一个页链接，如果不在set中就加入并解析
            if link.url not in self.page_link:
                self.page_link.add(link.url)
                yield Request(link.url,callback=self.parse_page)
        #对于每一个文章链接，如果不在content_link集合中就加入并解析
        for link in self.rules['content'].extract_links(response):
            if link.url not in self.content_link:
                self.content_link.add(link.url)
                yield Request(link.url,callback=self.parse_content)
    #用于解析每一页网页并找到文章链接
    def parse_page(self,response):
        for link in self.rules['page'].extract_links(response):
            if link.url not in self.page_link:
                self.page_link.add(link.url)
                yield Request(link.url,callback=self.parse_page)

        for link in self.rules['content'].extract_links(response):
            if link.url not in self.content_link:
                self.content_link.add(link.url)
                yield Request(link.url,callback=self.parse_content)
    #解析文章内容，找到标题还有内容
    def parse_content(self,response):
        item=JobboleItem()
        sel=Selector(response)
        title=sel.xpath('//title/text()').extract()[0]
        item['title']=title
        item['content']=response.body
        return item
