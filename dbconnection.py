import psycopg2
from psycopg2 import OperationalError


class DbConnection:
    def __init__(self, config):
        self.dbname = config.dbname
        self.user = config.user
        self.password = config.password
        self.host = config.host
        self.prefix = config.dbtableprefix
        self.conn = None

        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host
            )
        except OperationalError as e:
            print(f"Ошибка подключения к PostgreSQL: {e}")
            raise

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

    def test(self):
        if not self.conn:
            return False

        try:
            cur = self.conn.cursor()
            cur.execute("DROP TABLE IF EXISTS test CASCADE")
            cur.execute("CREATE TABLE test(test integer)")
            cur.execute("INSERT INTO test(test) VALUES(1)")
            self.conn.commit()
            cur.execute("SELECT * FROM test")
            result = cur.fetchall()
            cur.execute("DROP TABLE test")
            self.conn.commit()
            return (result[0][0] == 1)
        except Exception as e:
            print(f"Ошибка теста соединения: {e}")
            return False