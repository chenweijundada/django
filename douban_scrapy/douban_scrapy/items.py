# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    img_url = scrapy.Field()
    director = scrapy.Field()
    actor = scrapy.Field()
    year = scrapy.Field()
    country = scrapy.Field()
    type_ = scrapy.Field()
    rate = scrapy.Field()
    # quote = scrapy.Field()
