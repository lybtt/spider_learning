# -*- coding: utf-8 -*-
import re

import scrapy
import pymongo
from longzu5.items import Longzu5Item
from longzu5.settings import MONGO_DB, MONGO_URI, MONGO_TABLE



class LongzuSpider(scrapy.Spider):
    name = 'longzu'
    allowed_domains = ['www.yunxs.com']
    start_urls = ['http://www.yunxs.com/longzu5/']

    def parse(self, response):
        article_urls = response.xpath('//div[@class="list_box"]').css('a::attr(href)').extract()
        article_titles = response.xpath('//div[@class="list_box"]').css('li').css('a::text').extract()
        self.articles = dict(zip(article_urls, article_titles))
        self.paixu = dict(zip(range(10000), self.articles))
        self.exited_url_list = self.get_exited_url()
        for article_url, article_title in self.articles.items():
            article_url_com = response.urljoin(article_url)
            if article_url_com in self.exited_url_list:
                print('文章 {} 已存在'.format(self.articles[article_url]))
            else:
                yield scrapy.Request(url=article_url_com, callback=self.parse_content)

    def parse_content(self, response):
        content = []
        contents = response.xpath('//div[@class="box_box"]/text()').extract()
        for i in contents:
            content.append(i.replace('\xa0','').strip('\r\n'))
        old_url = re.search('.*?longzu5/(.*)', response.url).group(1)
        title = self.articles[old_url]
        item = Longzu5Item()
        item['title'] = title
        item['content'] = content
        item['url'] = response.url
        for number, url in self.paixu.items():
            if url == old_url:
                item['number'] = number
        yield item

    def get_exited_url(self, ):
        client = pymongo.MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        # collections = db.collection_names()   输出所有的collection名字
        neir = db.get_collection(MONGO_TABLE)
        """
        neir1 = neir.find_one()  # 输出第一个
        neirongs = neir.find()
        for i in neirongs:
            print(i.keys())
        """
        # 查询url字段,并将数据设置成集合
        exited_url_list = set()
        for x in neir.find({}, {"_id": 0, "url": 1}):
            exited_url_list.add(x['url'])
        return exited_url_list