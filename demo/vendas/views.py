from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Cliente, Pedido, Fornecedor, Produto, Pagamento, Itens_Pedido

def index(request):
    return render(request, 'vendas/index.html')

def cadastro_cliente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        telefone = request.POST.get('telefone')

        cliente = Cliente(nome=nome, cpf=cpf, telefone=telefone)
        cliente.save()

        return render(request, 'vendas/cadastro_cliente.html', {'sucesso': True})

    return render(request, 'vendas/cadastro_cliente.html')

def criar_novo_fornecedor(request):
    if request.method == 'POST':
        nome_fornecedor = request.POST.get('nome_fornecedor')
        email = request.POST.get('email')
        telefone_fornecedor = request.POST.get('telefone_fornecedor')

        fornecedor = Fornecedor(nome_fornecedor=nome_fornecedor, email=email, telefone_fornecedor=telefone_fornecedor)
        fornecedor.save()

        return render(request, 'vendas/criar_novo_fornecedor.html', {'sucesso': True})

    return render(request, 'vendas/criar_novo_fornecedor.html')

def criar_registro_do_produto(request):
    sucesso = False

    fornecedores = Fornecedor.objects.all()

    if request.method == 'POST':
        idfornecedor = request.POST.get('idfornecedor')
        nome_produto = request.POST.get('nome_produto')
        preco = request.POST.get('preco')
        estoque = request.POST.get('estoque')

        try:
            fornecedor = Fornecedor.objects.get(id_fornecedor=idfornecedor)
            produtos = Produto(idfornecedor=fornecedor, nome_produto=nome_produto, preco=preco, estoque=estoque)
            produtos.save()
            sucesso = True
        except Fornecedor.DoesNotExist:
            # Fornecedor nao encontrado]
            sucesso = False

        return render(request, 'vendas/criar_registro_do_produto.html', {
        'fornecedores': fornecedores,
        'sucesso': sucesso
        })

    return render(request, 'vendas/criar_registro_do_produto.html', {
        'fornecedores': fornecedores,
        'sucesso': sucesso
    })

def registrar_novo_pedido(request):
    clientes = Cliente.objects.all()
    sucesso = False
    id_pedido = None

    if request.method == 'POST':
        nome_cliente = request.POST.get('id_cliente')  # o campo no select envia o nome
        data_pedido = request.POST.get('data_pedido')

        try:
            cliente = Cliente.objects.get(nome=nome_cliente)
        except Cliente.DoesNotExist:
            cliente = None

        if cliente:
            pedido = Pedido(idcliente=cliente, data_pedido=data_pedido, total=0)
            pedido.save()

            sucesso = True
            id_pedido = pedido.id_pedido

            return render(request, 'vendas/registrar_novo_pedido.html', {
                'clientes': clientes,
                'sucesso': sucesso,
                'id_pedido': id_pedido
            })

    return render(request, 'vendas/registrar_novo_pedido.html', {
        'clientes': clientes,
        'sucesso': sucesso
    })



def verificar_pagamento(request, id_pedido):
    sucesso = False
    pedido = Pedido.objects.get(id_pedido=id_pedido)
    itens_query = Itens_Pedido.objects.filter(idpedido=id_pedido)

    itens = []
    for item in itens_query:
        produto = item.idproduto
        subtotal = produto.preco * item.quantidade
        itens.append({
            'nome_produto': produto.nome_produto,
            'quantidade': item.quantidade,
            'preco_unitario': produto.preco,
            'subtotal': subtotal
        })

    if request.method=='POST':
        metodo_de_pagamento = request.POST.get('metodo_pagamento')
        status_do_pagamento = request.POST.get('status_pagamento')

        try:
            valor = pedido.total
            pagamento = Pagamento(idpedido=pedido, valor=valor, metodo_de_pagamento=metodo_de_pagamento, status_pagamento=status_do_pagamento)
            pagamento.save()
            sucesso = True
        except Pedido.DoesNotExist:
            # Fornecedor nao encontrado
            sucesso = False

        return render(request, 'vendas/verificar_pagamento.html', {
            'pedido': pedido,
            'sucesso': sucesso,
            'itens': itens
        })

    return render(request, 'vendas/verificar_pagamento.html', {
            'pedido': pedido,
            'sucesso': sucesso,
            'itens': itens
    })


def adicionar_itens(request, id_pedido):
    inserido = False
    pedido = Pedido.objects.get(id_pedido=id_pedido)
    produtos = Produto.objects.all()
    itens = []

    if request.method == 'POST':
        id_produto = request.POST.get('id_produto')
        quantidade = int(request.POST.get('quantidade'))

        produto = Produto.objects.get(id_produto=id_produto)

        # Criar o item no banco de dados
        Itens_Pedido.objects.create(
            idpedido=pedido,
            idproduto=produto,  
            quantidade=quantidade
        )

        # Recalcular o total do pedido
        itens_query = Itens_Pedido.objects.filter(idpedido=pedido)

        for item in itens_query:    
            produto = item.idproduto
            subtotal = produto.preco * item.quantidade
            itens.append({
                'nome_produto': produto.nome_produto,
                'quantidade': item.quantidade,
                'preco_unitario': produto.preco,
                'subtotal': subtotal
            })

        # Atualizar o total do pedido
        total = sum(item['subtotal'] for item in itens)
        pedido.total = total
        pedido.save()

        inserido = True

    return render(request, 'vendas/adicionar_itens.html', {
        'pedido': pedido,
        'produtos': produtos,
        'inserido': inserido,
        'itens': itens
    })

def olhar_tabelas(request):
    return render(request, 'vendas/olhar_tabelas.html')

def ver_clientes(request):
    clientes = Cliente.objects.all()

    return render(request, 'vendas/ver_clientes.html', {
        'clientes': clientes
    })


def ver_pedidos(request):
    pedidos = Pedido.objects.all()
    dados = []

    for pedido in pedidos:
        cliente = pedido.idcliente
        itens = Itens_Pedido.objects.filter(idpedido=pedido)
        pagamento = Pagamento.objects.filter(idpedido=pedido).first()  # pode não existir ainda

        for item in itens:
            dados.append({ 
                'id_pedido': pedido.id_pedido,
                'nome_cliente': cliente.nome,
                'data_pedido': pedido.data_pedido,
                'id_produto': item.idproduto.nome_produto,
                'quantidade': item.quantidade,
                'metodo_pagamento': pagamento.metodo_de_pagamento if pagamento else '---',
                'status_pagamento': pagamento.status_pagamento if pagamento else '---',
                'total': pedido.total
            })

    return render(request, 'vendas/ver_pedidos.html', {'dados': dados})

def ver_fornecedores(request):
    fornecedores = Fornecedor.objects.all()

    return render(request, 'vendas/ver_fornecedores.html', {
        'fornecedores': fornecedores
    })

def ver_produtos(request):
    produtos = Produto.objects.all()

    return render(request, 'vendas/ver_produtos.html', {
        'produtos': produtos
    })