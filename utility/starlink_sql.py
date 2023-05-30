# 操作starlink数据库
# TODO: 优化批量insert, update的效率

import mysql.connector

class starlink_db:
    def __connect(self):
        """ private

        """
        try:
            conn = mysql.connector.connect(
                user='mysql',
                host='127.0.0.1',
                database='starlink',
                password='wuyanbo1607+'
            )
        except:
            exit(1)

        print("--- Connect Success")
        return conn


    def __init__(self) -> None:
        self.conn = self.__connect()

    def __del__(self):
        self.conn.close()
        print("--- connection close")


    def select(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        res = cursor.fetchall()

        return res
    
    def insert(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()

    def update(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()


    def table_struct_cp(self, orig, new):
        """ 仅拷贝表结构
        
        """
        query = 'CREATE TABLE {} LIKE {}'.format(new, orig)
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()


    def rename(self, old, new):
        """ 重命名数据表
        
        TODO: 处理请求失败
        """
        query = "RENAME TABLE {} TO {}".format(old, new)
        cursor = self.conn.cursor()
        cursor.execute(query)


    def clear(self, table):
        """ 清空数据表
        
        """
        query = "TRUNCATE TABLE {}".format(table)
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()


def test():
    pass


if __name__ == "__main__":
    test()
