# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from datetime import datetime

from weibo_scrapy import settings
from weibo_scrapy.items import UserInfoItem, UserRelationItem


class AddCreateTimePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, UserInfoItem):
            item['create_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return item


class WeiboScrapyPipeline(object):
    def __init__(self):
        conn = pymongo.MongoClient(host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
        db = conn[settings.MONGODB_DB]
        self.collection = db[UserInfoItem.collection]

    def process_item(self, item, spider):
        if isinstance(item, UserInfoItem):
            self.collection.update({'id': item['id']}, {'$set': dict(item)}, upsert=True)
        elif isinstance(item, UserRelationItem):
            self.collection.update({'id': item['id']},
                                   {'$addToSet': {
                                        'follows': {'$each': item['follows']},
                                        'followers': {'$each': item['followers']},
                                   }},
                                   upsert=True)
        return item
