import psycopg2
from tabulate import tabulate

def mostrar_resultado(cursor, descricao):
    resultados = cur.fetchall()
    colunas = [desc[0] for desc in cursor.description]
    print(f"\n{descricao}")
    print(tabulate(resultados, headers=colunas, tablefmt="grid"))


#connect to the db
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="85016244",
    host="localhost",
    port="5432"
)
print("Conexao estabelecida com sucesso!")

#cursor
cur = conn.cursor()

# 1. Utilizar os comandos relacionados com datas, tais como year, mouth, day e etc;
cur.execute("""
    SELECT * FROM pedidos
    WHERE data_pedido < DATE '2025-04-30';
""")
mostrar_resultado(cur, "Pedidos feitos no mês de maio de 2025")


cur.execute("""
    SELECT * FROM PEDIDOS
    WHERE EXTRACT(YEAR FROM data_pedido) = 2025;
""")
mostrar_resultado(cur, "Pedidos feitos no ano de 2025")


cur.execute("""
    SELECT * FROM PEDIDOS
    WHERE EXTRACT(MONTH FROM data_pedido) = 4;
""")
mostrar_resultado(cur, "Pedidos feitos no mes de abril")

# 2. Realizar consultas com operadores relacionais e operadores lógicos;
cur.execute("""
    SELECT * FROM pagamento
    WHERE valor >= 2500.0;
""")
mostrar_resultado(cur, "Pedidos com valores acima ou iguais a R$ 5500,00")


cur.execute("""
    SELECT * FROM cliente
    where nome LIKE '%a%';
""")
mostrar_resultado(cur, "Selecionando cliente que possuem letra 'a' no nome")


cur.execute("""
    SELECT * FROM produtos
    WHERE preco >= 500 AND preco <= 2000;
""")
mostrar_resultado(cur, "Produtos que possuem valores entre R$500 e R$1500")


# 3. Fazer junções entre tabelas por chave estrangeira e primária
cur.execute("""
    SELECT pedidos.idcliente, itens_pedido.idpedido, pedidos.data_pedido, pedidos.total 
    FROM itens_pedido
    INNER JOIN pedidos ON itens_pedido.idpedido = pedidos.id_pedido
;""")
mostrar_resultado(cur, "Consultado tabelas de pedidos e itens_pedido de acordo com os ids")


cur.execute("""
        SELECT itens_pedido.idpedido, itens_pedido.idproduto, produtos.nome_produto, produtos.idfornecedor,
        itens_pedido.quantidade, produtos.preco 
        FROM itens_pedido
        RIGHT JOIN produtos ON itens_pedido.idproduto = produtos.id_produto
;""")
mostrar_resultado(cur, "Consultando os produtos utilizando right join")

# 4. Utilizar alias tanto na projeção quanto na declaração de tabelas;
cur.execute("""
        SELECT 
        c.nome AS nome_cliente,
        p.nome_produto AS nome_produto,
        ip.quantidade AS qtd,
        pg.metodo_de_pagamento AS metodo_pagamento,
        pg.status_pagamento AS status_pagamento,
        pg.valor AS valor_total
    FROM 
        Pedidos pd
    JOIN 
        Cliente c ON pd.idcliente = c.id_cliente
    JOIN 
        Itens_Pedido ip ON pd.id_pedido = ip.idpedido
    JOIN 
        Produtos p ON ip.idproduto = p.id_produto
    JOIN 
        Pagamento pg ON pd.id_pedido = pg.idpedido;
""")
mostrar_resultado(cur, "Listando pedidos com nome do cliente, nome do produto, quantidade, metodo de pagamento, status e valor total")


# 5. Aplicar comandos ALL e DISTINCT e realizar agrupamentos GROUP BY
cur.execute("""
    SELECT DISTINCT metodo_de_pagamento
    FROM pagamento;
""")
mostrar_resultado(cur, "Exibindo todos os metodos de pagamentos unicos")

cur.execute("""
    SELECT
        status_pagamento,
        COUNT(*) AS total_pedidos
    FROM
        pagamento
    GROUP BY
        status_pagamento; 
""")
mostrar_resultado(cur, "Quantidade de pedidos por status de pagamento")

cur.execute("""
    SELECT * 
    FROM pagamento
    WHERE valor > ALL (SELECT valor FROM pagamento WHERE metodo_de_pagamento = 'Pix');
""")
mostrar_resultado(cur,"Pagamentos com valor maior que todos os do método Pix")

# 6. Fazer consultas com os comandos de conjuntos UNION, INTERSECTION, EXCEPT;
print("\nUNION:")
cur.execute("""
    SELECT nome FROM CLIENTE
    UNION
    SELECT nome_fornecedor FROM fornecedor;
""")
mostrar_resultado(cur, "Cliente e Fornecedores (sem repeticao)")

print("\nINTERSECTION: Nomes que aparecem como cliente e fornecedor")
cur.execute("""
    SELECT nome FROM cliente
    INTERSECT
    SELECT nome_fornecedor FROM fornecedor;
""")
mostrar_resultado(cur, "Nomes em comum (cliente e fornecedor)")

print("\nEXCEPT:")
cur.execute("""
    SELECT nome FROM cliente
    EXCEPT
    SELECT nome_fornecedor FROM fornecedor;
""")
mostrar_resultado(cur, "Clientes que nao sao fornecedores")


#7 .Utilizar operadores between e like
print("\nBetween")
cur.execute("""
            SELECT * FROM 
            fornecedor WHERE
            id_fornecedor BETWEEN 2 and 4
            """)
mostrar_resultado(cur, "Fornecedores com id entre 2 e 4")


print("\nLike")
cur.execute("""
            SELECT *FROM
            cliente WHERE nome
            LIKE '%c%'
            """)

mostrar_resultado(cur, "Clientes que tem a letra c")
cur.execute("""
            SELECT *FROM
            cliente WHERE nome
            LIKE 'c%'
            """)
mostrar_resultado(cur, "Clientes que comecam com a letra c")


print("\nOrderBY")
#8 OrderBY  crescente e decrescente
cur.execute(""" 
            SELECT *FROM 
            produtos ORDER BY
            nome_produto
            """)
mostrar_resultado(cur, "Produtos ordenados em ordem alfabetica ,Crescente:")

print("\n")
cur.execute(""" 
            SELECT *FROM 
            produtos ORDER BY
            nome_produto DESC
            """)

mostrar_resultado(cur, "Decrescente:")

#9. Utilizando os comandos IS e NOT IS
print("\nIS E NOT IS")
cur.execute("""
        SELECT *FROM fornecedor
        WHERE email IS NULL    
            """)
mostrar_resultado(cur, "Fornecedores que tem email nulo:")

cur.execute("""
        SELECT *FROM fornecedor
        WHERE email IS NOT NULL    
            """)
print("\n")
mostrar_resultado(cur, "Fornecedores que nao possuem email nulo:")

#10 . Utilizando IN,ANY E ALL
cur.execute("""
            SELECT *FROM fornecedor
            where id_fornecedor IN(
                SELECT id_fornecedor FROM produtos
            )
            """)
print("\nIN")
mostrar_resultado(cur, "Fornecedores que possuem produtos :")

cur.execute("""
            SELECT *FROM produtos
            where preco > ANY(
            SELECT preco FROM produtos
            WHERE idfornecedor = 1    
            )
            """)
print("\nANY")
mostrar_resultado(cur, "Fornecedores que possuem produtos  com preco maior que o primeiro fornecedor:")

cur.execute("""
            SELECT *FROM produtos
            where preco > ALL(
            SELECT preco FROM produtos
            WHERE idfornecedor = 2    
            )
            """)
print("\nALL")
mostrar_resultado(cur, "Fornecedores que possuem produtos com preco maior que o segundo fornecedor:")


print("\n")
#11. EXISTS E UNIQUE
cur.execute("""
            SELECT *FROM fornecedor f
            WHERE EXISTS(
                SELECT 1 FROM produtos p
                WHERE p.idfornecedor = f.id_fornecedor 
            )
            """)
mostrar_resultado(cur, "Fornecedores que possuem amo menos um produto cadastrado:")

#12. Comandos AVG, MIN, MAX, SUM, COUNT.
print("\nAVG")
cur.execute("""
            SELECT AVG(preco) AS media_preco FROM produtos
            """)
mostrar_resultado(cur, "Media de preco entre os produtos: ")

print("\nMIN")

cur.execute("""
            SELECT MIN(preco) AS menor_preco FROM produtos
            """)
mostrar_resultado(cur, "Menor preco entre os produtos: ")

print("\nSUM")
cur.execute("""
            SELECT SUM(preco) AS soma_dos_precos FROM produtos
            """)
mostrar_resultado(cur, "Soma dos precos entre os produtos: ")

print("\nCount")
cur.execute("""
            SELECT COUNT(preco) AS numero_de_produtos FROM produtos
            """)
mostrar_resultado(cur, "Total de  Produtos: ")

#commit the transiction
# conn.commit()

#close cursor
cur.close()
conn.close()