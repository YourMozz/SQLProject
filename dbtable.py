from dbconnection import *

class DbTable:
    dbconn = None

    def __init__(self):
        return

    def table_name(self):
        return self.dbconn.prefix + "table"

    def columns(self):
        return {"test": ["integer", "PRIMARY KEY"]}

    def column_names(self):
        return sorted(self.columns().keys(), key = lambda x: x)

    def primary_key(self):
        return ['id']

    def column_names_without_id(self):
        res = sorted(self.columns().keys(), key = lambda x: x)
        if 'id' in res:
            res.remove('id')
        return res

    def table_constraints(self):
        return []

    def create(self):
        sql = "CREATE TABLE " + self.table_name() + "("
        arr = [k + " " + " ".join(v) for k, v in sorted(self.columns().items(), key = lambda x: x[0])]
        sql += ", ".join(arr + self.table_constraints())
        sql += ")"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return

    def drop(self):
        sql = "DROP TABLE IF EXISTS " + self.table_name()
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return

    def first(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()        

    def last(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join([x + " DESC" for x in self.primary_key()])
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()

    def all(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def insert_one(self, *args, **kwargs):
        try:
            if self.table_name().endswith("Categories"):
                if len(args) == 1 and not kwargs:
                    name = args[0]
                else:
                    name = kwargs.get('name', args[0] if args else None)

                if not name:
                    raise ValueError("Не указано название категории")

                sql = f"INSERT INTO {self.table_name()}(name) VALUES(%s)"
                params = (name,)

            elif self.table_name().endswith("Medicine"):
                category_id = kwargs.get('category_id', args[0] if args else None)
                name = kwargs.get('name', args[1] if len(args) > 1 else None)
                dosage = kwargs.get('dosage', args[2] if len(args) > 2 else None)
                volume = kwargs.get('volume', args[3] if len(args) > 3 else None)
                producer = kwargs.get('producer', args[4] if len(args) > 4 else None)
                is_prescription = kwargs.get('is_prescription', args[5] if len(args) > 5 else None)
                price = kwargs.get('price', args[6] if len(args) > 6 else None)

                if None in (category_id, name, dosage, volume, producer, is_prescription, price):
                    raise ValueError("Не все обязательные поля указаны")

                sql = f"""INSERT INTO {self.table_name()}(
                    category_id, name, dosage, volume, producer, is_prescription, price
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                params = (category_id, name, dosage, volume, producer, is_prescription, price)

            else:
                raise ValueError(f"Неизвестный тип таблицы: {self.table_name()}")

            cur = self.dbconn.conn.cursor()
            cur.execute(sql, params)
            self.dbconn.conn.commit()
            return True

        except Exception as e:
            self.dbconn.conn.rollback()
            print(f"\nОшибка при добавлении записи: повтор. Попробуйте еще раз")
            return False
