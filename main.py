import psycopg2

#connect to the db
conn = psycopg2.connect(
    dbname="teste",
    user="postgres",
    password="database123",
    host="localhost",
    port="5432"
)
print("Conexao estabelecida com sucesso!")

#cursor
cur = conn.cursor()

cur.execute("""CREATE TABLE teste (
    id_teste serial primary key,
    nome_teste varchar(100)
);""")


#commit the transiction
conn.commit()

#close cursor
cur.close()
conn.close()