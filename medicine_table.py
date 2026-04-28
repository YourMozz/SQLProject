from dbtable import *


class MedicineTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "Medicine"

    def columns(self):
        return {
            "medicine_id": ["serial", "PRIMARY KEY"],
            "category_id": ["integer", "NOT NULL"],
            "name": ["text", "NOT NULL"],
            "dosage": ["text", "NOT NULL"],
            "volume": ["text", "NOT NULL"],
            "producer": ["text", "NOT NULL"],
            "is_prescription": ["boolean", "NOT NULL"],
            "price": ["integer", "NOT NULL"]
        }

    def primary_key(self):
        return ['medicine_id']

    def table_constraints(self):
        return [
            "UNIQUE (name, dosage, volume, producer)",
            "FOREIGN KEY (category_id) REFERENCES " + self.dbconn.prefix + "Categories(category_id)"
        ]

    def all_by_category_id(self, category_id, offset=0, limit=5):
        try:
            sql = f"""
            SELECT * FROM {self.table_name()} 
            WHERE category_id = %s 
            ORDER BY medicine_id 
            LIMIT %s OFFSET %s
            """
            cur = self.dbconn.conn.cursor()
            cur.execute(sql, (category_id, limit, offset))
            return cur.fetchall()
        except Exception as e:
            print(f"Ошибка при получении списка лекарств: {e}")
            self.dbconn.conn.rollback()
            return []

    def count_by_category_id(self, category_id):
        sql = "SELECT COUNT(*) FROM " + self.table_name() + " WHERE category_id = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (category_id,))
        return cur.fetchone()[0]

    def find_by_position(self, num):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY " + ", ".join(self.primary_key())
        sql += " LIMIT 1 OFFSET %(offset)s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"offset": num - 1})
        return cur.fetchone()