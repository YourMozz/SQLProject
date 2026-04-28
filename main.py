import sys
from tabulate import tabulate
sys.path.append('tables')

from project_config import *
from dbconnection import *
from categories_table import *
from medicine_table import *


class Main:
    config = None
    connection = None

    def __init__(self):
        try:
            self.config = ProjectConfig()
            self.connection = DbConnection(self.config)
            if not self.connection.conn:
                print("Не удалось установить соединение с базой данных!")
                raise SystemExit(1)

            DbTable.dbconn = self.connection
            self.current_category_id = -1
            self.current_page = 0
            self.current_medicine_page = 0
        except Exception as e:
            print(f"Ошибка инициализации: {e}")
            raise SystemExit(1)

    def _print_table(self, headers, data):
        print(tabulate(data, headers=headers, tablefmt="grid", stralign="left", numalign="left"))

    def contains_sql_keywords(self, user_input):
        sql_keywords = ['delete', 'insert', 'select', 'drop', 'update', 'alter', 'create', 'table']
        user_input_lower = user_input.lower()
        return any(keyword in user_input_lower for keyword in sql_keywords)

    def db_init(self):
        ct = CategoriesTable()
        mt = MedicineTable()
        ct.create()
        mt.create()
        return

    def db_insert_somethings(self):
        ct = CategoriesTable()
        mt = MedicineTable()

        ct.insert_one(name="Антибиотики")
        ct.insert_one(name="Обезболивающие")
        ct.insert_one(name="Противовоспалительное")
        ct.insert_one(name="Антигистаминные")
        ct.insert_one(name="Противоотечные")
        ct.insert_one(name="Антидепрессанты")
        ct.insert_one(name="Противовирусные")
        ct.insert_one(name="Гормональные")
        ct.insert_one(name="Пробиотики")
        ct.insert_one(name="Жаропонижающее")

        mt.insert_one(
            category_id=1,
            name="Амоксициллин",
            dosage="500 мг",
            volume="10 таблеток",
            producer="Фармстандарт",
            is_prescription=True,
            price=350
        )

        mt.insert_one(
            category_id=1,
            name="Азитромицин",
            dosage="250 мг",
            volume="6 капсул",
            producer="Вертекс",
            is_prescription=True,
            price=450
        )

        mt.insert_one(
            category_id=2,
            name="Ибупрофен",
            dosage="200 мг",
            volume="20 таблеток",
            producer="Биохимик",
            is_prescription=False,
            price=120
        )

        mt.insert_one(
            category_id=2,
            name="Ибупрофен",
            dosage="200 мг",
            volume="20 таблеток",
            producer="ФармКом",
            is_prescription=False,
            price=150.00
        )

        mt.insert_one(
            category_id=1,
            name="Амоксициллин",
            dosage="500 мг",
            volume="10 капсул",
            producer="БиоФарм",
            is_prescription=True,
            price=300.00
        )

        mt.insert_one(
            category_id=3,
            name="Витамин C",
            dosage="1000 мг",
            volume="30 таблеток",
            producer="HealthPlus",
            is_prescription=False,
            price=250.00
        )

        mt.insert_one(
            category_id=4,
            name="Лоратадин",
            dosage="10 мг",
            volume="15 таблеток",
            producer="Аллергостоп",
            is_prescription=False,
            price=180.00
        )

        mt.insert_one(
            category_id=5,
            name="Псевдоэфедрин",
            dosage="30 мг",
            volume="10 таблеток",
            producer="Респира",
            is_prescription=True,
            price=200.00
        )

        mt.insert_one(
            category_id=6,
            name="Флуоксетин",
            dosage="20 мг",
            volume="30 капсул",
            producer="Психофарм",
            is_prescription=True,
            price=450.00
        )

        mt.insert_one(
            category_id=7,
            name="Осельтамивир",
            dosage="75 мг",
            volume="10 капсул",
            producer="ВирусШелд",
            is_prescription=True,
            price=700.00
        )

        mt.insert_one(
            category_id=8,
            name="Левотироксин",
            dosage="50 мкг",
            volume="30 таблеток",
            producer="ГормонЛаб",
            is_prescription=True,
            price=350.00
        )

        mt.insert_one(
            category_id=9,
            name="Лактобактерин",
            dosage="2 млрд КОЕ",
            volume="10 флаконов",
            producer="БиоКультура",
            is_prescription=False,
            price=400.00
        )

        mt.insert_one(
            category_id=10,
            name="Фуросемид",
            dosage="40 мг",
            volume="20 таблеток",
            producer="ДиуретикФарм",
            is_prescription=True,
            price=220.00
        )

    def db_drop(self):
        mt = MedicineTable()
        ct = CategoriesTable()
        mt.drop()
        ct.drop()
        return

    def show_main_menu(self):
        menu = """Добро пожаловать в систему учета лекарств!
Основное меню (выберите цифру в соответствии с необходимым действием): 
    1 - просмотр категорий лекарств;
    2 - сброс и инициализация таблиц;
    9 - выход."""
        print(menu)
        return

    def read_next_step(self):
        return input("=> ").strip()

    def after_main_menu(self, next_step):
        if next_step == "2":
            self.db_drop()
            self.db_init()
            self.db_insert_somethings()
            print("Таблицы созданы заново!")
            return "0"
        elif next_step != "1" and next_step != "9":
            print("Выбрано неверное число! Повторите ввод!")
            return "0"
        else:
            return next_step

    def show_categories(self, page=0, per_page=5):
        self.current_category_id = -1

        try:
            offset = page * per_page
            sql = f"SELECT * FROM {CategoriesTable().table_name()} ORDER BY category_id LIMIT {per_page} OFFSET {offset}"
            cur = self.connection.conn.cursor()
            cur.execute(sql)
            categories = cur.fetchall()
            total = self.get_total_categories()

            headers = ["№", "Название категории"]
            data = []
            for i, category in enumerate(categories, start=offset + 1):
                data.append([i, category[1]])

            print("\nСписок категорий лекарств:")
            if not data:
                print("Нет доступных категорий")
            else:
                print(tabulate(
                    data,
                    headers=headers,
                    tablefmt="grid",
                    stralign="left"
                ))

            total_pages = max(1, ((total - 1) // per_page) + 1)
            print(f"\nСтраница {page + 1} из {total_pages}")

            menu = """Дальнейшие операции: 
        0 - возврат в главное меню;
        3 - добавление новой категории;
        4 - удаление категории;
        5 - просмотр лекарств в категории;
        6 - следующая страница;
        7 - предыдущая страница;
        9 - выход."""
            print(menu)

        except Exception as e:
            print(f"Ошибка при загрузке категорий: {e}")
            self.connection.conn.rollback()

    def get_total_categories(self):
        sql = f"SELECT COUNT(*) FROM {CategoriesTable().table_name()}"
        cur = self.connection.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()[0]

    def after_show_categories(self, next_step):
        while True:
            if next_step == "3":
                self.show_add_category()
                return "1"
            elif next_step == "4":
                self.show_delete_category()
                return "1"
            elif next_step == "5":
                next_step = self.show_medicines_by_category()
            elif next_step == "6":
                total = self.get_total_categories()
                total_pages = max(1, ((total - 1) // 5) + 1)
                if self.current_page + 1 < total_pages:
                    self.current_page += 1
                else:
                    print("Это последняя страница!")
                return "1"
            elif next_step == "7":
                if self.current_page > 0:
                    self.current_page -= 1
                else:
                    print("Это первая страница!")
                return "1"
            elif next_step not in ("0", "1", "9"):
                return "1"
            else:
                return next_step

    def show_add_category(self):
        name = input("Введите название новой категории (1 - отмена): ").strip()
        if name == "1":
            return

        if self.contains_sql_keywords(name):
            print("Ввод содержит запрещённые слова!")
            return

        while len(name) == 0:
            name = input("Название не может быть пустым! Введите название (1 - отмена): ").strip()
            if name == "1":
                return
            if self.contains_sql_keywords(name):
                print("Ввод содержит запрещённые слова!")
                return

        try:
            CategoriesTable().insert_one(name)
            print("Категория успешно добавлена!")
        except Exception as e:
            print(f"Ошибка при добавлении категории: повтор")
            self.connection.conn.rollback()

    def show_delete_category(self):
        num = input("Укажите номер категории для удаления (0 - отмена): ").strip()
        while len(num) == 0:
            num = input("Пустая строка. Повторите ввод! Укажите номер категории (0 - отмена): ").strip()

        if num == "0":
            return

        try:
            num = int(num)

            sql = f"SELECT category_id FROM {CategoriesTable().table_name()} ORDER BY category_id"
            cur = self.connection.conn.cursor()
            cur.execute(sql)
            all_categories = cur.fetchall()

            if num < 1 or num > len(all_categories):
                print(f"Категории с номером {num} не существует!")
                return

            category_id = all_categories[num - 1][0]

            sql = f"SELECT COUNT(*) FROM {MedicineTable().table_name()} WHERE category_id = %s"
            cur.execute(sql, (category_id,))
            count = cur.fetchone()[0]

            if count > 0:
                print("Нельзя удалить категорию, в которой есть лекарства!")
                return

            sql = f"DELETE FROM {CategoriesTable().table_name()} WHERE category_id = %s"
            cur.execute(sql, (category_id,))
            self.connection.conn.commit()
            print("Категория успешно удалена!")

            total = self.get_total_categories()
            per_page = 5
            total_pages = max(1, ((total - 1) // per_page) + 1)
            if self.current_page >= total_pages and self.current_page > 0:
                self.current_page -= 1

        except ValueError:
            print("Введите корректный номер!")
        except Exception as e:
            print(f"Ошибка при удалении категории: {e}")
            self.connection.conn.rollback()

    def validate_dosage(self, dosage):
        import re
        pattern = r'^\d+\s+(мг|мкг|млрд КОЕ)$'
        if not re.match(pattern, dosage):
            return False
        amount = int(re.search(r'^\d+', dosage).group())
        return 1 <= amount <= 1000

    def validate_volume(self, volume):
        import re
        pattern = r'^\d+\s+(таблеток|капсул|флаконов|ампул|таблетка|таблетки)$'
        if not re.match(pattern, volume):
            return False
        amount = int(re.search(r'^\d+', volume).group())
        return 0 < amount < 100

    def show_medicines_by_category(self, page=0):
        if self.current_category_id == -1:
            while True:
                try:
                    sql = f"SELECT category_id, name FROM {CategoriesTable().table_name()} ORDER BY category_id"
                    cur = self.connection.conn.cursor()
                    cur.execute(sql)
                    all_categories = cur.fetchall()

                    if not all_categories:
                        print("Нет доступных категорий!")
                        return "1"


                    choice = input("\nВведите номер категории (0 - отмена): ").strip()
                    if choice == "0":
                        return "1"

                    if not choice.isdigit():
                        print("Ошибка: нужно ввести число!")
                        continue

                    choice_num = int(choice)
                    if choice_num < 1 or choice_num > len(all_categories):
                        print(f"Ошибка: номер должен быть от 1 до {len(all_categories)}!")
                        continue

                    self.current_category_id = all_categories[choice_num - 1][0]
                    self.current_category_name = all_categories[choice_num - 1][1]
                    self.current_medicine_page = 0
                    break

                except Exception as e:
                    print(f"Ошибка при выборе категории: {e}")
                    self.connection.conn.rollback()
                    return "1"

        try:
            offset = page * 5
            medicines = MedicineTable().all_by_category_id(self.current_category_id, offset, 5)
            total = MedicineTable().count_by_category_id(self.current_category_id)

            headers = ["№", "Название", "Дозировка", "Форма выпуска", "Производитель", "Рецептурный", "Цена"]
            data = []
            for i, med in enumerate(medicines, start=1 + offset):
                prescription = "Да" if med[3] else "Нет"
                data.append([
                    i,
                    med[4],
                    med[1],
                    med[7],
                    med[6],
                    prescription,
                    f"{med[5]} руб."
                ])

            print(f"\nЛекарства в категории: {self.current_category_name}")
            if not data:
                print("В этой категории пока нет лекарств")
            else:
                print(tabulate(
                    data,
                    headers=headers,
                    tablefmt="grid",
                    stralign="left",
                    numalign="left",
                    maxcolwidths=[5, 20, 10, 15, 15, 10, 10]
                ))

            total_pages = max(1, ((total - 1) // 5) + 1)
            print(f"\nСтраница {page + 1} из {total_pages}")

            menu = """\nДальнейшие операции:
        0 - возврат в главное меню;
        1 - возврат к списку категорий;
        6 - добавление нового лекарства;
        7 - удаление лекарства;
        8 - редактирование лекарства;
        9 - следующая страница;
        10 - предыдущая страница;
        11 - выход."""
            print(menu)

            while True:
                next_step = self.read_next_step()

                if next_step == "6":
                    self.show_add_medicine()
                    return "5"
                elif next_step == "7":
                    self.show_delete_medicine()
                    return "5"
                elif next_step == "8":
                    self.show_edit_medicine()
                    return "5"
                elif next_step == "9":
                    if (page + 1) * 5 < total:
                        return self.show_medicines_by_category(page + 1)
                    else:
                        print("Это последняя страница!")
                        return "5"
                elif next_step == "10":
                    if page > 0:
                        return self.show_medicines_by_category(page - 1)
                    else:
                        print("Это первая страница!")
                        return "5"
                elif next_step in ("0", "1", "11"):
                    if next_step == "0":
                        self.current_category_id = -1
                        return "0"
                    elif next_step == "1":
                        self.current_category_id = -1
                        return "1"
                    else:
                        return "11"
                else:
                    print("Неверный выбор! Повторите ввод.")

        except Exception as e:
            print(f"Ошибка при отображении лекарств: {e}")
            self.connection.conn.rollback()
            return "1"

    def show_add_medicine(self):
        print("\nДобавление нового лекарства:")

        name = input("Название лекарства (1 - отмена): ").strip()
        if name == "1":
            return

        if self.contains_sql_keywords(name):
            print("Ввод содержит запрещённые слова!")
            return

        while len(name) == 0:
            name = input("Название не может быть пустым! Введите название (1 - отмена): ").strip()
            if name == "1":
                return
            if self.contains_sql_keywords(name):
                print("Ввод содержит запрещённые слова!")
                return

        dosage = input("Дозировка (например, '500 мг'): ").strip()
        if self.contains_sql_keywords(dosage):
            print("Ввод содержит запрещённые слова!")
            return

        while not self.validate_dosage(dosage):
            dosage = input("Неверный формат дозировки! Пример: '500 мг' (1 - отмена): ").strip()
            if dosage == "1":
                return
            if self.contains_sql_keywords(dosage):
                print("Ввод содержит запрещённые слова!")
                return

        volume = input("Форма выпуска (например, '10 таблеток'): ").strip()
        if self.contains_sql_keywords(volume):
            print("Ввод содержит запрещённые слова!")
            return

        while not self.validate_volume(volume):
            volume = input("Неверный формат! Пример: '10 таблеток' (1 - отмена): ").strip()
            if volume == "1":
                return
            if self.contains_sql_keywords(volume):
                print("Ввод содержит запрещённые слова!")
                return

        producer = input("Производитель: ").strip()
        if self.contains_sql_keywords(producer):
            print("Ввод содержит запрещённые слова!")
            return

        while len(producer) == 0:
            producer = input("Производитель не может быть пустым! Введите производителя (1 - отмена): ").strip()
            if producer == "1":
                return
            if self.contains_sql_keywords(producer):
                print("Ввод содержит запрещённые слова!")
                return

        prescription = input("Рецептурный препарат? (да/нет): ").strip().lower()
        if self.contains_sql_keywords(prescription):
            print("Ввод содержит запрещённые слова!")
            return

        while prescription not in ['да', 'нет']:
            prescription = input("Введите 'да' или 'нет' (1 - отмена): ").strip().lower()
            if prescription == "1":
                return
            if self.contains_sql_keywords(prescription):
                print("Ввод содержит запрещённые слова!")
                return

        is_prescription = prescription == 'да'

        price = input("Цена (руб.): ").strip()
        if self.contains_sql_keywords(price):
            print("Ввод содержит запрещённые слова!")
            return

        while not price.isdigit() or int(price) <= 0:
            price = input("Цена должна быть положительным числом! Введите цену (1 - отмена): ").strip()
            if price == "1":
                return
            if self.contains_sql_keywords(price):
                print("Ввод содержит запрещённые слова!")
                return

        price = int(price)

        try:
            MedicineTable().insert_one(
                    category_id=self.current_category_id,
                    name=name,
                    dosage=dosage,
                    volume=volume,
                    producer=producer,
                    is_prescription=is_prescription,
                    price=price
            )
            print("Лекарство успешно добавлено!")
        except Exception as e:
            print(f"Ошибка при добавлении лекарства: повтор")

    def show_delete_medicine(self):
        num = input("Укажите номер строки с лекарством для удаления (0 - отмена): ").strip()
        while len(num) == 0 or len(num)>10:
            if len(num) == 0:
                num = input("Пустая строка. Повторите ввод! Укажите номер строки (0 - отмена): ").strip()
            else:
                num = input("Такого нет. Введите корректный номер1 (0 - отмена): ").strip()

        if num == "0":
            return


        try:
            num = int(num)
            offset = self.current_medicine_page * 5

            sql = f"""
            SELECT medicine_id FROM {MedicineTable().table_name()} 
            WHERE category_id = %s 
            ORDER BY medicine_id 
            LIMIT 1 OFFSET {offset + num - 1}
            """
            cur = self.connection.conn.cursor()
            cur.execute(sql, (self.current_category_id,))
            medicine = cur.fetchone()

            if not medicine:
                print("Лекарство с указанным номером не найдено!")
                return

            medicine_id = medicine[0]

            sql = f"DELETE FROM {MedicineTable().table_name()} WHERE medicine_id = %s"
            cur.execute(sql, (medicine_id,))
            self.connection.conn.commit()
            print("Лекарство успешно удалено!")
        except ValueError:
            print("Введите корректный номер!")
        except Exception as e:
            print(f"Ошибка при удалении лекарства: {e}")

    def show_edit_medicine(self):
        num = input("Укажите номер строки с лекарством для редактирования (0 - отмена): ").strip()
        while len(num) == 0:
            num = input("Пустая строка. Повторите ввод! Укажите номер строки (0 - отмена): ").strip()

        if num == "0":
            return

        try:
            num = int(num)
            offset = self.current_medicine_page * 5

            sql = f"""
            SELECT * FROM {MedicineTable().table_name()} 
            WHERE category_id = %s 
            ORDER BY medicine_id 
            LIMIT 1 OFFSET {offset + num - 1}
            """
            cur = self.connection.conn.cursor()
            cur.execute(sql, (self.current_category_id,))
            medicine = cur.fetchone()

            if not medicine:
                print("Лекарство с указанным номером не найдено!")
                return

            print("\nТекущие данные лекарства:")
            print(f"1. Название: {medicine[4]}")
            print(f"2. Дозировка: {medicine[1]}")
            print(f"3. Форма выпуска: {medicine[7]}")
            print(f"4. Производитель: {medicine[6]}")
            print(f"5. Рецептурный: {'Да' if medicine[3] else 'Нет'}")
            print(f"6. Цена: {medicine[5]} руб.")
            print("0. Отмена")

            field = input("Выберите поле для редактирования (1-6): ").strip()
            if self.contains_sql_keywords(field):
                print("Ввод содержит запрещённые слова!")
                return

            while field not in ['0', '1', '2', '3', '4', '5', '6']:
                field = input("Неверный выбор! Выберите поле (1-6) или 0 для отмены: ").strip()
                if self.contains_sql_keywords(field):
                    print("Ввод содержит запрещённые слова!")
                    return

            if field == "0":
                return

            new_value = None
            if field == "1":
                new_value = input("Новое название: ").strip()
                if self.contains_sql_keywords(new_value):
                    print("Ввод содержит запрещённые слова!")
                    return
                while len(new_value) == 0:
                    new_value = input("Название не может быть пустым! Введите название: ").strip()
                    if self.contains_sql_keywords(new_value):
                        print("Ввод содержит запрещённые слова!")
                        return
            elif field == "2":
                new_value = input("Новая дозировка (например, '500 мг'): ").strip()
                if self.contains_sql_keywords(new_value):
                    print("Ввод содержит запрещённые слова!")
                    return
                while not self.validate_dosage(new_value):
                    new_value = input("Неверный формат дозировки! Пример: '500 мг': ").strip()
                    if self.contains_sql_keywords(new_value):
                        print("Ввод содержит запрещённые слова!")
                        return
            elif field == "3":
                new_value = input("Новая форма выпуска (например, '10 таблеток'): ").strip()
                if self.contains_sql_keywords(new_value):
                    print("Ввод содержит запрещённые слова!")
                    return
                while not self.validate_volume(new_value):
                    new_value = input("Неверный формат! Пример: '10 таблеток': ").strip()
                    if self.contains_sql_keywords(new_value):
                        print("Ввод содержит запрещённые слова!")
                        return
            elif field == "4":
                new_value = input("Новый производитель: ").strip()
                if self.contains_sql_keywords(new_value):
                    print("Ввод содержит запрещённые слова!")
                    return
                while len(new_value) == 0:
                    new_value = input("Производитель не может быть пустым! Введите производителя: ").strip()
                    if self.contains_sql_keywords(new_value):
                        print("Ввод содержит запрещённые слова!")
                        return
            elif field == "5":
                new_value = input("Рецептурный препарат? (да/нет): ").strip().lower()
                if self.contains_sql_keywords(new_value):
                    print("Ввод содержит запрещённые слова!")
                    return
                while new_value not in ['да', 'нет']:
                    new_value = input("Введите 'да' или 'нет': ").strip().lower()
                    if self.contains_sql_keywords(new_value):
                        print("Ввод содержит запрещённые слова!")
                        return
                new_value = new_value == 'да'
            elif field == "6":
                new_value = input("Новая цена (руб.): ").strip()
                if self.contains_sql_keywords(new_value):
                    print("Ввод содержит запрещённые слова!")
                    return
                while not new_value.isdigit() or int(new_value) <= 0:
                    new_value = input("Цена должна быть положительным числом! Введите цену: ").strip()
                    if self.contains_sql_keywords(new_value):
                        print("Ввод содержит запрещённые слова!")
                        return
                new_value = int(new_value)

            field_names = ['name', 'dosage', 'volume', 'producer', 'is_prescription', 'price']
            sql = f"""
            UPDATE {MedicineTable().table_name()} 
            SET {field_names[int(field) - 1]} = %s 
            WHERE medicine_id = %s
            """
            cur.execute(sql, (new_value, medicine[0]))
            self.connection.conn.commit()
            print("Лекарство успешно обновлено!")
        except ValueError:
            print("Введите корректный номер!")
        except Exception as e:
            print(f"Ошибка при редактировании лекарства: {e}")

    def main_cycle(self):
        current_menu = "0"
        next_step = None
        while (current_menu != "9" and current_menu != "11"):
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == "1":
                self.show_categories(self.current_page)
                next_step = self.read_next_step()
                current_menu = self.after_show_categories(next_step)
            elif current_menu == "5":
                current_menu = self.show_medicines_by_category(self.current_medicine_page)
        print("До свидания!")
        return


m = Main()
m.main_cycle()