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
    WHERE data_pedido < DATE '2025-04-30';
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
print("\n Pedidos com valores acima ou iguais a R$ 5500,00")
cur.execute("""
    SELECT * FROM pagamento
    WHERE valor >= 2500.0;
""")

valores = cur.fetchall()

for linha in valores:
    print(linha)

print("\nSelecionando cliente que possuem letra 'a' no nome:")
cur.execute("""
    SELECT * FROM cliente
    where nome LIKE '%a%';
""")

clientes = cur.fetchall()
for linha in clientes:
    print(linha)

print("\nProdutos que possuem valores entre R$500 e R$1500")
cur.execute("""
    SELECT * FROM produtos
    WHERE preco >= 500 AND preco <= 2000;
""")

produtos = cur.fetchall()
for linha in produtos:
    print(linha)


# 3. Fazer junções entre tabelas por chave estrangeira e primária
print("\nConsultado tabelas de pedidos e itens_pedido de acordo com os ids: ")
cur.execute("""
    SELECT pedidos.idcliente, itens_pedido.idpedido, pedidos.data_pedido, pedidos.total 
    FROM itens_pedido
    INNER JOIN pedidos ON itens_pedido.idpedido = pedidos.id_pedido
;""")

pedidos_relacionados = cur.fetchall()

for linha in pedidos_relacionados:
    print(linha)


print("\nConsultando os produtos utilizando right join:")
cur.execute("""
        SELECT itens_pedido.idpedido, itens_pedido.idproduto, produtos.nome_produto, produtos.idfornecedor,
        itens_pedido.quantidade, produtos.preco 
        FROM itens_pedido
        RIGHT JOIN produtos ON itens_pedido.idproduto = produtos.id_produto
;""")

p = cur.fetchall()

for linha in p:
    print(linha)

#commit the transiction
# conn.commit()

#close cursor
cur.close()
conn.close()