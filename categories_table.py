from dbtable import *
class CategoriesTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "Categories"

    def columns(self):
        return {
            "category_id": ["serial", "PRIMARY KEY"],
            "name": ["text", "NOT NULL"]
        }

    def primary_key(self):
        return ['category_id']

    def table_constraints(self):
        return ["UNIQUE (name)"]

    def insert_one(self, name):
        sql = f"INSERT INTO {self.table_name()}(name) VALUES(%s)"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (name,))
        self.dbconn.conn.commit()

    def find_by_position(self, num):
        sql = f"SELECT * FROM {self.table_name()} ORDER BY {', '.join(self.primary_key())} LIMIT 1 OFFSET %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (num - 1,))
        return cur.fetchone()