# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db, mongo_table):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_table = mongo_table

    @classmethod
    def from_crawler(cls, crawler):
        """
            获取settings 里的全局配置， 传递给init
        :param crawler:
        :return:
        """
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_table=crawler.settings.get('MONGO_TABLE')
        )

    def open_spider(self, spider):
        """
            在spider开启时候连接mongo 数据库
        :param spider:
        :return:
        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        """
            处理数据
        :param item:
        :param spider:
        :return:
        """
        self.db[self.mongo_table].update({'url': item['url']}, {'$set': item}, True)
        # 第一个参数查询条件， $set设置键  第三个参数设置查询有就更新，没有就插入
        return item

    def close_spider(self, spider):
        """
            在spider 关闭的时候关闭mongo 数据库
        :param spider:
        :return:
        """
        self.client.close()
