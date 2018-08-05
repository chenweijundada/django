import json

import scrapy
from scrapy import Selector, Request

from weibo_scrapy.items import UserInfoItem


class WeiboSpider(scrapy.Spider):
    name = 'weibo'

    # 1669879400
    # 用户信息api https://m.weibo.cn/api/container/getIndex?type=all&value=1669879400&containerid=1005051669879400 #topnav[]=1&topnav[]=1&wvr[]=6&wvr[]=6&topsug[]=1&topsug[]=1&jumpfrom=weibocom
    # 他的关注api https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_1669879400&luicode=10000011&lfid=1076031669879400
    # 他的粉丝api https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_1669879400&luicode=10000011&lfid=1076031669879400
    # start_urls = ['https://m.weibo.cn/api/container/getIndex?type=all&value=1669879400&containerid=1005051669879400']

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
        # item['avatar_hd'] = data['avatar_hd']
        # item['cover_image_phone'] = data['cover_image_phone']
        # item['description'] = data['description']
        # item['follow_count'] = data['follow_count']
        # item['followers_count'] = data['followers_count']
        # item['gender'] = data['gender']
        # item['id'] = data['id']
        # item['profile_url'] = data['profile_url']
        # item['screen_name'] = data['screen_name']
        # item['statuses_count'] = data['statuses_count']
        # item['verified'] = data['verified']
        # item['verified_reason'] = data['verified_reason']

        return item