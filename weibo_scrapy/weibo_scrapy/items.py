# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserInfoItem(scrapy.Item):
    # 保存在MongoDB中的文档名
    collection = 'user_info'

    # 高清大头像
    avatar_hd = scrapy.Field()
    # 背景封面
    cover_image_phone = scrapy.Field()
    # 描述
    description = scrapy.Field()
    # 关注人数
    follow_count = scrapy.Field()
    # 粉丝人数
    followers_count = scrapy.Field()
    # 性别
    gender = scrapy.Field()
    # id
    id = scrapy.Field()
    # 主页url
    profile_url = scrapy.Field()
    # 用户名
    screen_name = scrapy.Field()
    # statuses_count
    statuses_count = scrapy.Field()
    # 是否认证
    verified = scrapy.Field()
    # 认证原因
    verified_reason = scrapy.Field()
    # 创建时间
    create_time = scrapy.Field()


class UserRelationItem(scrapy.Item):
    # 保存在MongoDB中的文档名
    collection = 'user_info'

    id = scrapy.Field()

    # 粉丝列表
    followers = scrapy.Field()
    # 关注列表
    follows = scrapy.Field()
