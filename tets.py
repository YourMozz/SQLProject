import psycopg2

conn = psycopg2.connect(
    dbname="lab7",
    user="postgres",
    password="egor2005p",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()
cursor.execute("SELECT * from public.medicine;")
print(cursor.fetchone())

conn.close()