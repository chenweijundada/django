import pymysql
from itcast_scrapy import settings


class MySqlHelper(object):
    """MySQLHelper"""
    def __init__(self):
        """
        构造器
        :param connect_config: 连接配置，dict
        """
        self.connect_config = {
            'host': settings.MYSQL_HOST,
            'user': settings.MYSQL_USER,
            'password': settings.MYSQL_PASSWORD,
            'port': int(settings.MYSQL_PORT),
            'database': settings.MYSQL_DB,
            'charset': 'utf8',
            'autocommit': False,
            'cursorclass': pymysql.cursors.DictCursor
        }
        self.conn = None
        self.cursor = None

    def connect_db(self):
        """创建数据库连接"""
        self.conn = pymysql.connect(**self.connect_config)
        # self.cursor = self.conn.cursor()

    def close_db(self):
        """关闭数据库连接"""
        # if self.cursor:
        #     self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute_dql(self, sql, *, param=None):
        """
        执行dql操作，即 select 语句
        :param sql: sql语句，string
        :param param: 参数列表，dict
        :return: 查询结果，tuple
        """
        res = ''
        try:
            self.connect_db()
            with self.conn.cursor() as self.cursor:
                self.cursor.execute(sql, param)
                res = self.cursor.fetchall()
        except BaseException as e:
            print(e)
        finally:
            self.close_db()
        return res

    def execute_dml(self, sql, *, param=None):
        """
        执行dql操作，即 update、delete、insert 语句
        :param sql: sql语句，string
        :param param: 参数列表，dict
        :return: 查询结果，int [1：成功，0：正常失败，-1：错误失败]
        """
        try:
            self.connect_db()
            with self.conn.cursor() as self.cursor:
                count = self.cursor.execute(sql, param)
                self.conn.commit()
                if count:
                    res = 1
                else:
                    res = 0
        except BaseException as e:
            print(e)
            self.conn.rollback()
            res = -1
        finally:
            self.close_db()
        return res


def main():
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'hrs',
        'port': 3306,
        'charset': 'utf8',
        'autocommit': False,
        'cursorclass': pymysql.cursors.DictCursor  # cursorclass设置cursor游标的类型，这里设置的是dict类型
    }
    sqlhelper = MySqlHelper(config)
    sql = 'select dno, dname, dloc from tbDept where dno=%(no)s'
    param = {
        'no': 10
    }
    res = sqlhelper.execute_dql(sql, param=param)
    print(res)

    sql = 'insert into TbDept values (%(no)s, %(name)s, %(loc)s)'
    param = {
        'no': 88,
        'name': 'sda88',
        'loc': 'DSfcz88'
    }
    res = sqlhelper.execute_dml(sql, param=param)
    print(res)


if __name__ == '__main__':
    main()
