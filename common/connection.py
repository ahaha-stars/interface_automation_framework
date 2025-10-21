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
            if not res:
                return []

            keys = list(res[0].keys()) if res else []
            values = [list(item.values()) for item in res]

            result = [keys] + values
            return result

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
        try:
            # 执行插入语句（参数化查询，避免SQL注入）
            # params为参数列表，例如插入(name, age)时，params=(张三, 20)
            self.cursor.execute(sql)

            # 提交事务（插入操作必须提交才会生效）
            self.conn.commit()

            # 获取受影响的行数（通常为1，因为单条插入）
            affected_rows = self.cursor.rowcount

            # 如果表有自增ID，可返回最后插入的ID（不同数据库语法可能不同）
            # 例如MySQL用 lastrowid，PostgreSQL用 returning 子句，这里以MySQL为例
            last_insert_id = self.cursor.lastrowid

            # 返回受影响行数和自增ID（按需选择）
            return {
                "affected_rows": affected_rows,
                "last_insert_id": last_insert_id
            }

        except Exception as e:
            # 发生异常时回滚事务，避免数据不一致
            self.conn.rollback()
            print(f"插入操作失败：{str(e)}")
            return None


    def updata(self,sql):
        pass

    def delete(self,sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            logs.info('删除成功')
        except Exception as e:
            logs.error(e)
        finally:
            self.close()

if __name__ == '__main__':
    conn = ConnectMysql()
    sql = 'select * from tb_vehicle_info limit 5'
    print(conn.query(sql))

