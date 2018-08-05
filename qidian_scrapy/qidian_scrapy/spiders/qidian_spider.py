import scrapy
from scrapy import Selector


class QidianSpider(scrapy.Spider):
    # 启动项目制定的name参数
    name = 'Qidian'
    # allowed_domains = ["qidian.com"]
    # 需要爬取的页面
    start_urls = ['https://www.qidian.com/']

    def parse(self, response):
        html = Selector(response=response)
        type_list = html.xpath('//*[@id="classify-list"]/dl/dd/a/cite/span/i/text()').extract()
        href_list = html.xpath('//*[@id="classify-list"]/dl/dd/a/@href').extract()
        # print('12345' + response)
        print(type_list)
        print(href_list)
        return response
    yield item
