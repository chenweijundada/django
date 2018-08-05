import json

import scrapy
from scrapy import Selector, Request

from weibo_scrapy.items import UserInfoItem


class WeiboSpider(scrapy.Spider):
    name = 'weibo2'

    # start_urls = ['https://m.weibo.cn/api/container/getIndex?type=all&value=1669879400&containerid=1005051669879400']

    user_follower_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&featurecode=20000320&since_id={page}'
    user_follow_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&featurecode=20000320&type=all&page={page}'
    user_url = 'https://m.weibo.cn/api/container/getIndex?type=all&value={uid}&containerid=100505{uid}'
    user_id_list = ['3952070245', '1669879400', '1192515960', '1158709993', '1778742953']

    def start_requests(self):
        for uid in self.user_id_list:
            yield Request(url=self.user_url.format(uid=uid), callback=self.parse)

    def parse(self, response):
        datas = json.loads(response.text)
        data = datas.get('data').get('userInfo')
        item = UserInfoItem()

        user_params = ['avatar_hd', 'cover_image_phone', 'description', 'follow_count', 'followers_count',
                       'gender', 'id', 'profile_url', 'screen_name', 'statuses_count', 'verified', 'verified_reason']

        for k in user_params:
            item[k] = data[k]

        # return item
        for i in range(1, 11):
            yield Request(url=self.user_follow_url.format(uid=item['id'], page=str(i)),
                          callback=self.parse_follow,
                          meta={'metadata': item, 'page': i})

    def parse_follow(self, response):
        datas = json.loads(response.text)
        if response.meta['page'] == 1:
            data = datas.get('data').get('cards')[4].get('card_group')
        else:
            data = datas.get('data').get('cards')[0].get('card_group')
        print(response.url, response.meta['page'])
        follows = []
        for follow in data:
            tmp = {}
            tmp['scheme'] = follow['scheme']
            tmp['follow_id'] = follow['user']['id']
            tmp['screen_name'] = follow['user']['screen_name']
            tmp['locate_page'] = response.meta['page']
            follows.append(tmp)
        metadata = response.meta['metadata']
        metadata['follows'] = follows

        for i in range(1, 251):
            yield Request(url=self.user_follower_url.format(uid=metadata['id'], page=str(i)),
                          callback=self.parse_follower,
                          meta={'metadata': metadata, 'page': i})

    def parse_follower(self, response):
        datas = json.loads(response.text)
        data = datas.get('data').get('cards')[0].get('card_group')

        followers = []
        for follower in data:
            tmp = {}
            tmp['scheme'] = follower['scheme']
            tmp['follow_id'] = follower['user']['id']
            tmp['screen_name'] = follower['user']['screen_name']
            tmp['locate_page'] = response.meta['page']
            followers.append(tmp)
        metadata = response.meta['metadata']
        metadata['followers'] = followers

        return metadata