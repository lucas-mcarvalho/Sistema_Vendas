from django.db import models

# Create your models here.
#METODO PARA SALVAR UM CLIENTE NO BANCO DE DADOS
class Cliente(models.Model):
    '''
    GERANDO A CHAVE AUTOMATICAMENTE'''
    id_cliente = models.AutoField(primary_key=True) 
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)  # Formato: 000.000.000-00
    telefone = models.CharField(max_length=20)

    class Meta:
        managed = False  # Django NÃO vai tentar criar ou alterar essa tabela
        db_table = 'cliente'  # nome EXATO da tabela no banco PostgreSQL

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    idcliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        db_column='idcliente'
    )
    data_pedido = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'pedidos'

    def __str__(self):
        return self.Pedido.id_pedido
    
class Fornecedor(models.Model):
    id_fornecedor = models.AutoField(primary_key=True)
    nome_fornecedor = models.CharField(max_length=100)
    email = models.CharField(max_length=60)
    telefone_fornecedor = models.CharField(max_length=15)

    class Meta:
        managed = False 
        db_table = 'fornecedor'

    def __str__(self):
        return f"({self.id}) {self.nome_fornecedor}: {self.telefone_fornecedor}"
    
class Produto(models.Model):
    id_produto = models.AutoField(primary_key=True)
    idfornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.CASCADE,
        db_column='idfornecedor'
    )
    nome_produto = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()

    class Meta:
        managed = False  
        db_table = 'produtos'

    def __str__(self):
        return f"({self.id_produto}) {self.nome_produto}: Preco: {self.preco} Estoque: {self.estoque}"
    
class Itens_Pedido(models.Model):
    id = models.AutoField(primary_key=True)
    idpedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        db_column='idpedido'
    )

    idproduto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        db_column='idproduto'
    )

    quantidade = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'itens_pedido'

    def __str__(self):
        return f"Pedido: {self.idpedido} Produto: {self.idproduto} Quantidade: {self.quantidade}"

    
class Pagamento(models.Model):
    METODO_PAGAMENTO_CHOICES = [
        ('Cartão de Crédito', 'Cartão de Crédito'),
        ('Pix', 'Pix'),
        ('Boleto', 'Boleto'),
        ('Dinheiro', 'Dinheiro'),
    ]

    STATUS_PAGAMENTO_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Pago', 'Pago'),
        ('Cancelado', 'Cancelado'),
    ]

    id_pagamento = models.AutoField(primary_key=True)

    idpedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        db_column='idpedido'
    )

    valor = models.DecimalField(max_digits=10, decimal_places=2)

    metodo_de_pagamento = models.CharField(
        max_length=20,
        choices=METODO_PAGAMENTO_CHOICES
    )

    status_pagamento = models.CharField(
        max_length=10,
        choices=STATUS_PAGAMENTO_CHOICES
    )

    class Meta:
        managed = False  
        db_table = 'pagamento'

    def __str__(self):
        return f"ID do pedido: {self.idpedido} Valor: {self.valor} Metodo de Pagamento: {self.metodo_de_pagamento} Status do Pagamento: {self.status_pagamento}"