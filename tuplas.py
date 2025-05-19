import psycopg2

conn = psycopg2.connect(
    dbname="Vendas",
    user="postgres",
    password="database123",
    host="localhost",
    port="5432"
)
print("Conexao estabelecida com sucesso!")

#cursor
cur = conn.cursor()

cur.execute("""
    select * from fornecedor;
""")

resultados = cur.fetchall()

for linha in resultados:
    print(linha)

#commit the transiction
# conn.commit()

#close cursor
cur.close()
conn.close()