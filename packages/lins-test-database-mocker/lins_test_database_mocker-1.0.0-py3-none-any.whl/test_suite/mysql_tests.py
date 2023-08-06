from unittest import TestCase
from test_database import Mysql
from os import environ


class MysqlTestCase(TestCase):

    def setUp(self):
        self.mysql = Mysql()
        self.mysql.connect()

    def test_mysql_deve_se_conectar_corretamente(self):
        self.assertIn(f"{environ['MYSQL_HOST']}:{environ['MYSQL_PORT']}", self.mysql.connection.host_info)
        self.assertEqual(environ['MYSQL_DATABASE'], self.mysql.connection.db.decode('UTF-8'))

    def test_tabela_em_database_teste_deve_ser_criada(self):
        self.mysql.set_cursor()
        self.assertFalse(self.mysql.cursor.execute('SHOW TABLES'))
        self.mysql.cursor.execute('CREATE TABLE IF NOT EXISTS lins_mock_test (name VARCHAR(20))')
        self.assertTrue(self.mysql.cursor.execute('SHOW TABLES'))
        self.mysql.cursor.execute('DROP TABLE lins_mock_test')

    def test_dados_devem_ser_inseridos_na_tabela_teste(self):
        self.mysql.execute('CREATE TABLE IF NOT EXISTS lins_mock_test (name VARCHAR(20))')
        self.mysql.execute('INSERT INTO lins_mock_test VALUES ("Testing")')
        self.assertEqual({'name': 'Testing'}, self.mysql.execute('SELECT * FROM lins_mock_test', 'fetchone'))
        self.mysql.execute('DROP TABLE lins_mock_test')

    def test_lista_queries_deve_ser_executada(self):
        query_list = [
            'CREATE TABLE IF NOT EXISTS lins_mock_test (name VARCHAR(20))',
            'INSERT INTO lins_mock_test VALUES ("Testing")',
        ]
        self.mysql.execute_test_queries(query_list)
        self.assertEqual({'name': 'Testing'}, self.mysql.execute('SELECT * FROM lins_mock_test', 'fetchone'))
        self.mysql.execute('DROP TABLE lins_mock_test')

    def tearDown(self):
        self.mysql.connection.close()
