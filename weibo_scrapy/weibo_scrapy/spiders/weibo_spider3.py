import json

import scrapy
from scrapy import Selector, Request

from weibo_scrapy.items import UserInfoItem, UserRelationItem


class WeiboSpider(scrapy.Spider):
    name = 'weibo3'

    # start_urls = ['https://m.weibo.cn/api/container/getIndex?type=all&value=1669879400&containerid=1005051669879400']
    # 关注 https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{}&luicode=10000011&lfid=1076031669879400&featurecode=20000320&type=all&page=2
    # 粉丝 https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_1669879400&luicode=10000011&lfid=1076031669879400&featurecode=20000320&since_id=2

    # 粉丝url
    user_follower_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&since_id={page}'
    # 关注url
    user_follow_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}'
    # 个人信息url
    user_url = 'https://m.weibo.cn/api/container/getIndex?type=all&value={uid}&containerid=100505{uid}'
    user_id_list = ['3952070245', '1669879400', '1192515960', '1158709993', '1778742953']

    def start_requests(self):
        for uid in self.user_id_list:
            yield Request(url=self.user_url.format(uid=uid), callback=self.parse)

    def parse(self, response):
        """
        解析用户个人信息
        :param response:
        :return:
        """
        datas = json.loads(response.text)
        data = datas.get('data').get('userInfo')
        item = UserInfoItem()

        user_params = ['avatar_hd', 'cover_image_phone', 'description', 'follow_count', 'followers_count',
                       'gender', 'id', 'profile_url', 'screen_name', 'statuses_count', 'verified', 'verified_reason']

        for k in user_params:
            item[k] = data.get(k)

        yield item
        # 获取关注
        yield Request(url=self.user_follow_url.format(uid=item['id'], page=str(1)),
                      callback=self.parse_follow,
                      meta={'uid': item['id'], 'page': 1, 'type': 'follow'})
        # 获取用户粉丝
        yield Request(url=self.user_follower_url.format(uid=item['id'], page=str(1)),
                      callback=self.parse_follow,
                      meta={'uid': item['id'], 'page': 1, 'type': 'follower'})

    def parse_follow(self, response):
        """
        解析用户关注的人或者粉丝的信息
        :param response:
        :return:
        """
        datas = json.loads(response.text)
        if datas.get('ok'):
            data = datas.get('data').get('cards')[-1].get('card_group')

            for follow in data:
                user_info = follow['user']
                uid = user_info['id']
                yield Request(url=self.user_url.format(uid=uid), callback=self.parse)

            # 添加用户和关注人之间的关系
            follow_list = []
            for follow in data:
                user_info = follow['user']
                follow_list.append({'id': user_info['id'], 'screen_name': user_info['screen_name'], 'profile_url': user_info['profile_url']})

            user_relation = UserRelationItem()
            user_relation['id'] = response.meta.get('uid')
            if response.meta.get('type') == 'follow':
                user_relation['followers'] = []
                user_relation['follows'] = follow_list
            elif response.meta.get('type') == 'follower':
                user_relation['followers'] = follow_list
                user_relation['follows'] = []
            yield user_relation

            # 获取下一页的关注
            uid = response.meta.get('uid')
            page = int(response.meta.get('page')) + 1
            type_ = response.meta.get('type')
            if type_ == 'follow':
                yield Request(url=self.user_follow_url.format(uid=uid, page=page),
                              callback=self.parse_follow,
                              meta={'uid': uid, 'page': page, 'type': 'follow'})
            elif type_ == 'follower':
                yield Request(url=self.user_follower_url.format(uid=uid, page=page),
                              callback=self.parse_follow,
                              meta={'uid': uid, 'page': page, 'type': 'follower'})

    def parse_follower(self, response):
        """
        解析用户粉丝的信息
        :param response:
        :return:
        """
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