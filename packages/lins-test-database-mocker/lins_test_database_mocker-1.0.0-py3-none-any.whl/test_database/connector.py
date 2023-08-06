import pymysql.cursors
from os import environ


class Mysql:

    def connect(self, connection_params={}):
        connection = dict(
            host=environ.get('MYSQL_HOST', '127.0.0.1'),
            user=environ.get('MYSQL_USER', 'root'),
            password=environ.get('MYSQL_PASS', 'root'),
            db=environ.get('MYSQL_DATABASE', 'testing'),
            port=int(environ.get('MYSQL_PORT', '3306')),
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False,
            charset=environ.get('MYSQL_CHARSET', 'utf8mb4'),
        )
        connection.update(connection_params)
        self.connection = pymysql.connect(**connection)

    def set_cursor(self):
        self.cursor = self.connection.cursor()

    def execute(self, query, attr=None):
        self.set_cursor()
        self.cursor.execute(query)
        if attr:
            data = getattr(self.cursor, attr)()
            self.cursor.close()
            return data
        self.cursor.close()

    def execute_test_queries(self, query_list):
        self.set_cursor()
        for query in query_list:
            self.execute(query)
            self.connection.commit()
        self.cursor.close()
