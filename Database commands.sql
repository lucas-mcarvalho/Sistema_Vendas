-- Select nas tabelas
select * from cliente;
select * from fornecedor;
select * from pedidos;
select * from itens_pedido;
select * from produtos;
select * from pagamento;

-- Criação das tabelas (verificar os tipos delas)
create table cliente(
	id_cliente serial primary key,
	nome varchar(100),
	cpf varchar(11),
	telefone varchar(15)
);

create table pedidos(
	id_pedido serial primary key,
	idcliente integer,
	data_pedido date,
	total decimal,

	foreign key (idcliente) references cliente(id_cliente)
);

create table fornecedor(
	id_fornecedor serial primary key,
	nome_fornecedor varchar(100),
	email varchar(60),
	telefone_fornecedor varchar(15)
);

create table produtos(
	id_produto serial primary key,
	idfornecedor integer,
	nome_produto varchar(255),
	preco decimal,
	estoque integer,

	foreign key(idfornecedor) references fornecedor(id_fornecedor)
);

create table itens_pedido(
	id serial primary key,
	idpedido integer not null,
	idproduto integer not null,
	quantidade integer,

	foreign key (idpedido) references pedidos(id_pedido),
	foreign key (idproduto) references produtos(id_produto)
);

create table pagamento(
	id_pagamento serial primary key,
	idpedido integer,
	valor decimal,
	metodo_de_pagamento metodo_pagamento,
	status_pagamento status_pagamento_enum,

	foreign key(idpedido) references pedidos(id_pedido)
);

-- Inserção de valores nas tabelas

-- Criando novo cliente
insert into cliente(nome, cpf, telefone) values ('Marcelo', '12345678901', '11987654321');

-- Criando um fornecedor
insert into fornecedor(nome_fornecedor, email, telefone_fornecedor)
values ('Castor', 'castorcolchoes@gmail.com', '21998765432');

-- Criando um produto
insert into produtos(idfornecedor, nome_produto, preco, estoque)
values (1, 'Colchão Silver Star', '1099.99', 15);

-- Criando tipos para metodo_pagamento e status_pagamento
create type metodo_pagamento as ENUM('Cartão de Crédito', 'PIX', 'Boleto', 'Dinheiro');
create type status_pagamento_enum as ENUM('Pendente', 'Pago', 'Cancelado');

-- Criando novo pedido
insert into pedidos(idcliente, data_pedido, total) 
values (1, '14/04/2025', 1099.99);

-- Inserindo dado na tabela Itens_Pedido
insert into itens_pedido (idpedido, idproduto, quantidade)
values (1, 1, 1);

-- Inserindo novo pagamento
insert into pagamento (idpedido, valor, metodo_de_pagamento, status_pagamento)
values (1, 1099.99, 'PIX', 'Pago');

-- Tentando ler as tabelas com as informações necessárias de acordo com a relação inner join
select pedidos.idcliente, itens_pedido.idpedido, pedidos.data_pedido, pedidos.total from itens_pedido
inner join pedidos on itens_pedido.idpedido = pedidos.id_pedido;

-- Tentando ler as tabelas com as informações necessárias de acordo com a relação right join
select itens_pedido.idpedido, itens_pedido.idproduto, produtos.nome_produto, produtos.idfornecedor,
itens_pedido.quantidade, produtos.preco from itens_pedido
right join produtos on itens_pedido.idproduto = produtos.id_produto;



