# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

from douban_scrapy import settings


class DoubanScrapyPipeline(object):
    def __init__(self):
        conn = pymongo.MongoClient(host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
        db = conn[settings.MONGODB_DB]
        self.collection = db[settings.MONGODB_COLLECTION]

    def process_item(self, item, spider):
        print(item)
        data = dict({'title': item['title'], 'img_url': item['img_url'], 'director': item['director'], 'actor': item['actor'], 'year': item['year'], 'country': item['country'], 'type_': item['type_'], 'rate': item['rate']})  # , 'quote': item['quote']
        self.collection.insert(data)
        # return item
