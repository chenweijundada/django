from douyu_scrapy.items import DouyuItem


class DouyuPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, DouyuItem):
            with open('./' + item['name'] + '.jpg', 'wb') as fw:
                fw.write(item['img_con'])