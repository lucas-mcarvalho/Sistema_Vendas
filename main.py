import psycopg2

#connect to the db
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

# 1. Utilizar os comandos relacionados com datas, tais como year, mouth, day e etc;
print("\nPedidos feitos no mês de maio de 2025: ")
cur.execute("""
    SELECT * FROM pedidos
    WHERE data_pedido >= DATE '2025-05-01' AND data_pedido < DATE '2025-05-31';
""")

pedidos_maio_2025 = cur.fetchall()

for linha in pedidos_maio_2025:
    print(linha)

print("\nPedidos feitos no ano de 2025: ")
cur.execute("""
    SELECT * FROM PEDIDOS
    WHERE EXTRACT(YEAR FROM data_pedido) = 2025;
""")

pedidos_2025 = cur.fetchall()
for linha in pedidos_2025:
    print(linha)

print("\nPedidos feitos no mes de abril: ")
cur.execute("""
    SELECT * FROM PEDIDOS
    WHERE EXTRACT(MONTH FROM data_pedido) = 4;
""")

pedidos_abril = cur.fetchall()
for linha in pedidos_abril:
    print(linha)

# 2. Realizar consultas com operadores relacionais e operadores lógicos;


#commit the transiction
# conn.commit()

#close cursor
cur.close()
conn.close()