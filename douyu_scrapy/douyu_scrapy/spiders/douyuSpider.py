import json
import scrapy
from scrapy.http import Request
from douyu_scrapy.items import DouyuItem


class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ["itcast.cn"]

    offset = 0
    url = "http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset="
    start_urls = [url + str(offset)]

    def parse(self, response):
        data = json.loads(response.text)['data']

        for each in data:
            name = each['nickname']
            img_url = each['avatar_mid']
            print(img_url)
            yield Request(img_url, callback=self.get_content, meta={'name': name})

    def get_content(self, response):
        item = DouyuItem()
        print(response.content)
        item['img_con'] = response.content
        item['name'] = response.meta['name']
        # print(item['img_con'])
        yield item

        self.offset = self.offset + 20
        yield Request(self.url + str(self.offset), callback=self.parse)