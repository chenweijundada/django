from .mysqlHelper import MySqlHelper
from itcast_scrapy.items import ItcastItem


class ItcastPipeline(object):

    def process_item(self, item, spider):
        helper = MySqlHelper()
        if isinstance(item, ItcastItem):
            param = {
                'img_url': item['img_url']
            }
            res = helper.execute_dql('select * from itcast where it_img_url=%(img_url)s', param=param)
            if res:
                print('已经存在')
            else:
                param = {
                    'name': item['name'],
                    'img_url': item['img_url'],
                    'title': item['title'],
                    'info': item['info']
                }
                r = helper.execute_dml('insert into itcast (it_name, it_img_url, it_title, it_info) values '
                                       '(%(name)s, %(img_url)s, %(title)s, %(info)s)', param=param)
                if r:
                    print('存储成功')
                else:
                    print('存储失败')