import scrapy
from scrapy import Selector, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import Rule, CrawlSpider

from douban_scrapy.items import DoubanScrapyItem


class DoubanSpider2(CrawlSpider):
    name = 'Douban2'

    start_urls = [
        'https://movie.douban.com/top250'
    ]

    rules = [
        Rule(LinkExtractor(allow=r'https://movie.douban.com/top250.*'), callback='parse_item')
    ]

    def parse_item(self, response):
        html = Selector(response=response)

        # 电影名 //*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]
        titles = html.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]/text()').extract()

        # 电影封面 //*[@id="content"]/div/div[1]/ol/li/div/div[1]/a/img
        img_urls = html.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[1]/a/img/@src').extract()

        # 电影导演、主演、年份、国家、分类信息 //*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]
        director_actor_year_country_type = html.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()').extract()

        # 电影导演、主演
        directors_actors = [info.strip() for info in director_actor_year_country_type[::2]]
        directors, actors = [], []
        for info in directors_actors:
            directors.append(info.split('\xa0\xa0\xa0')[0].strip())
            actors.append(info.split('\xa0\xa0\xa0')[-1].strip())

        # 年份、国家、类型
        movie_infos = [info.strip().replace('\xa0', ' ') for info in director_actor_year_country_type[1::2]]
        years, countries, types = [], [], []
        for info in movie_infos:
            years.append(info.split('/')[0].strip())
            countries.append(info.split('/')[1].strip())
            types.append(info.split('/')[2].strip())

        # 电影评分 //*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/div/span[2]
        rates = html.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/div/span[2]/text()').extract()

        # 电影引用的名句 //*[@id="content"]/div/div[1]/ol/li[1]/div/div[2]/div[2]/p[2]/span
        # quotes = html.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[2]/span/text()').extract()

        for i in range(len(titles)):
            douban = DoubanScrapyItem()
            douban['title'] = titles[i]
            douban['img_url'] = img_urls[i]
            douban['director'] = directors[i]
            douban['actor'] = actors[i]
            douban['year'] = years[i]
            douban['country'] = countries[i]
            douban['type_'] = types[i]
            douban['rate'] = rates[i]
            # douban['quote'] = quotes[i]
            yield douban
