from common.recordlog import logs
from conf.operationConfig import OperationConfig
import pymysql
conf = OperationConfig()

class ConnectMysql():

    def __init__(self):

        mysql_conf = {
            'host': conf.get_mysql_conf('host'),
            'port': int(conf.get_mysql_conf('port')),
            'user': conf.get_mysql_conf('username'),
            'password': conf.get_mysql_conf('password'),
            'database': conf.get_mysql_conf('database')
        }
        try:
            self.conn = pymysql.connect(**mysql_conf,charset='utf8')
            print(self.conn)
            self.cursor = self.conn.cursor()
            print(self.cursor)
            logs.info("""成功连接到MYSQL数据库
            host:{host}
            port:{port}
            db:{database}""".format(**mysql_conf))
        except Exception as e:
            logs.error(e)

    def close(self):
        if self.conn and self.cursor:
            self.cursor.close()
            self.conn.close()

    def query(self,sql):
        """
        查询语句
        :param sql:  sql语句
        :return:
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            res = self.cursor.fetchall()
            return res
        except Exception as e:
            logs.error(e)
        finally:
            self.close()

    def insert(self,sql):
        """
        新增的sql语句
        :param sql:
        :return:
        """

    def updata(self,sql):
        pass

    def delete(self,sql):
        pass

if __name__ == '__main__':
    conn = ConnectMysql()
    sql = 'select * from tb_vehicle_info limit 5'
    print(conn.query(sql))

