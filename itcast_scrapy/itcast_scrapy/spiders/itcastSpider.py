import scrapy
from itcast_scrapy.items import ItcastItem


class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ["itcast.cn"]
    start_urls = ("http://www.itcast.cn/channel/teacher.shtml",)
    base_url = 'http://www.itcast.cn'

    def parse(self, response):
        divs = response.xpath('//div[@class="tea_con"]/div')
        print(len(divs))
        for div in divs:
            lis = div.xpath('ul/li')
            for li in lis:
                itcast = ItcastItem()

                img_url = li.xpath('img/@data-original').extract()
                name = li.xpath('div/h3/text()').extract()
                title = li.xpath('div/h4/text()').extract()
                info = li.xpath('div/p/text()').extract()

                itcast['img_url'] = self.base_url + img_url[0]
                itcast['name'] = name[0]
                itcast['title'] = title[0]
                itcast['info'] = info[0]
                yield itcast
                # items.append(itcast)

        # return items