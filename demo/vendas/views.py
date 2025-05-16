from django.shortcuts import render, get_object_or_404, redirect
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
        nome_fornecedor = request.POST.get('nome_fornecedor') or None
        email = request.POST.get('email') or None
        telefone_fornecedor = request.POST.get('telefone_fornecedor') or None

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

    # Total e desconto
    total_original = sum(item['subtotal'] for item in itens)
    desconto = 0
    if len(itens) >= 3:
        item_mais_barato = min(itens, key=lambda x: x['preco_unitario'])
        desconto = item_mais_barato['preco_unitario']
    
    total_com_desconto = total_original - desconto

    if request.method == 'POST':
        metodo_de_pagamento = request.POST.get('metodo_pagamento')
        status_do_pagamento = request.POST.get('status_pagamento')

    
        try:
            pagamento = Pagamento(
                idpedido=pedido,
                valor=total_com_desconto,  # APLICANDO o desconto aqui!
                metodo_de_pagamento=metodo_de_pagamento,
                status_pagamento=status_do_pagamento
            )
            pagamento.save()
            sucesso = True
        except Pedido.DoesNotExist:
            sucesso = False

        return render(request, 'vendas/verificar_pagamento.html', {
            'pedido': pedido,
            'sucesso': sucesso,
            'itens': itens,
            'total_original': total_original,
            'desconto': desconto,
            'total_com_desconto': total_com_desconto
        })

    return render(request, 'vendas/verificar_pagamento.html', {
        'pedido': pedido,
        'sucesso': sucesso,
        'itens': itens,
        'total_original': total_original,
        'desconto': desconto,
        'total_com_desconto': total_com_desconto
    })



def adicionar_itens(request, id_pedido):
    inserido = False
    terceiro_gratis = False  # <== novo
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

        inserido = True

    # Atualiza a lista de itens independente do POST
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

    # Verifica se o terceiro item acabou de ser adicionado
    if len(itens) == 3:
        terceiro_gratis = True

    return render(request, 'vendas/adicionar_itens.html', {
        'pedido': pedido,
        'produtos': produtos,
        'inserido': inserido,
        'itens': itens,
        'terceiro_gratis': terceiro_gratis  # passa para o template
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
    if request.method == 'POST':
        acao = request.POST.get("acao")
        id_fornecedor = request.POST.get("id_fornecedor")

        if acao == 'editar':
            return redirect('editar_fornecedor', id=id_fornecedor)
        elif acao == 'deletar':
            fornecedor = get_object_or_404(Fornecedor, pk=id_fornecedor)
            fornecedor.delete()
            return redirect('ver_fornecedores')

    fornecedores = Fornecedor.objects.all()

    return render(request, 'vendas/ver_fornecedores.html', {
        'fornecedores': fornecedores
    })

def ver_produtos(request):
    if request.method == 'POST':
        acao = request.POST.get("acao")
        id_produto = request.POST.get("id_produto")

        if acao == 'editar':
            return redirect('editar_produtos', id=id_produto)
        elif acao == 'deletar':
            produto = get_object_or_404(Produto, pk=id_produto)
            produto.delete()
            return redirect('ver_produtos')


    produtos = Produto.objects.all()

    return render(request, 'vendas/ver_produtos.html', {
        'produtos': produtos
    })


def gerenciar_clientes(request):
    clientes = Cliente.objects.all()
    if request.method == 'POST':
        # Obter o ID do cliente a ser deletado
        acao = request.POST['acao']
        id_cliente = request.POST.get('id_cliente')
        # Verificar se o id_cliente foi passado
        if acao == 'editar':
            return redirect('editar_cliente',id_cliente =id_cliente)
        if id_cliente:
            cliente = get_object_or_404(Cliente, id_cliente=id_cliente)
            cliente.delete()  # Deleta o cliente no banco de dados            
            # Após deletar, redireciona para a mesma página
    return render(request, 'vendas/gerenciar_clientes.html', {'clientes': clientes})


def editar_cliente(request, id_cliente):
    sucesso = False
    cliente = get_object_or_404(Cliente, pk=id_cliente)

    if request.method == 'POST':
        cliente.nome = request.POST['nome']
        cliente.cpf = request.POST['cpf']
        cliente.telefone = request.POST['telefone']
        cliente.save()
        sucesso = True
        return render(request, 'vendas/editar_cliente.html', {'cliente': cliente ,'sucesso': sucesso}) # redireciona para a mesma página

    return render(request, 'vendas/editar_cliente.html', {'cliente': cliente ,'sucesso': sucesso})


def editar_fornecedor(request, id):
    fornecedor = get_object_or_404(Fornecedor, pk=id)
    sucesso = False

    if request.method == 'POST':
        fornecedor.nome_fornecedor = request.POST.get('nome_fornecedor')
        fornecedor.email = request.POST.get('email')
        fornecedor.telefone_fornecedor = request.POST.get('telefone_fornecedor')
        fornecedor.save()
        sucesso = True

    return render(request, 'vendas/editar_fornecedor.html', {
        'fornecedor': fornecedor,
        'sucesso': sucesso
    })


def editar_produtos(request, id):
    produto = get_object_or_404(Produto, pk=id)
    fornecedores = Fornecedor.objects.all()  # ADICIONADO
    sucesso = False

    if request.method == 'POST':
        produto.nome_produto = request.POST.get('nome_produto')
        produto.idfornecedor = get_object_or_404(Fornecedor, pk=request.POST.get('idfornecedor'))
        produto.estoque = request.POST.get('estoque')
        produto.preco = request.POST.get('preco')
        produto.save()
        sucesso = True

    return render(request, 'vendas/editar_produtos.html', {
        'produto': produto,
        'fornecedores': fornecedores,  # ADICIONADO
        'sucesso': sucesso
    })
    
    
def escolher_acao_pedido(request, id_pedido):
    if request.method == 'POST':
        acao = request.POST.get('acao')
        if acao == 'editar':
            return redirect('editar_pedido', id=id_pedido)
        elif acao == 'deletar':
            # Corrigir o uso do id_pedido
            pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
            pedido.delete()
            return redirect('ver_pedidos')  # Aqui você pode ajustar a URL conforme necessário
    return redirect('ver_pedidos')  # Caso o método não seja POST, redireciona de volta

def editar_pedido(request, id):
    sucesso = False
    pedido = get_object_or_404(Pedido, id_pedido=id)
    item_pedido = Itens_Pedido.objects.filter(idpedido=pedido).first()
    clientes = Cliente.objects.all()
    produtos = Produto.objects.all()

    if request.method == "POST":
        print("Requisição POST recebida.")

        # Buscar cliente
        try:
            cliente = Cliente.objects.get(id_cliente=request.POST["nome_cliente"])
            pedido.idcliente = cliente
        except Cliente.DoesNotExist:
            print("Cliente não encontrado.")
            cliente = None

        # Buscar produto
        try:
            produto = Produto.objects.get(id_produto=request.POST["id_produto"])
        except Produto.DoesNotExist:
            print("Produto não encontrado.")
            produto = None

        # Validar e atribuir quantidade
        quantidade = request.POST.get("quantidade")
        if quantidade and quantidade.isdigit():
            quantidade = int(quantidade)
        else:
            quantidade = 1  # Valor padrão

        # Atualizar ou criar item de pedido
        if produto:
            item_pedido = Itens_Pedido.objects.filter(idpedido=pedido).first()
            if item_pedido:
                item_pedido.idproduto = produto
                item_pedido.quantidade = quantidade
                item_pedido.save()
            else:
                Itens_Pedido.objects.create(
                    idpedido=pedido,
                    idproduto=produto,
                    quantidade=quantidade
                )

        # Validar e atribuir data
        data_pedido = request.POST.get("data_pedido")
        if data_pedido:
            pedido.data_pedido = data_pedido
        else:
            print("Erro: Data do pedido não fornecida.")

        # Calcular total
        if produto and quantidade:
            pedido.total = produto.preco * quantidade

        try:
            pedido.save()
            sucesso = True
            print("Pedido salvo com sucesso.")
        except Exception as e:
            print(f"Erro ao salvar o pedido: {e}")

        return render(request, "vendas/editar_pedido.html", {
            "pedido": pedido,
            "clientes": clientes,
            "produtos": produtos,
            'sucesso': sucesso
        })

    return render(request, "vendas/editar_pedido.html", {
        "pedido": pedido,
        "clientes": clientes,
        "produtos": produtos,
    })
    
def editar_pagamentos(request):
    pagamentos = Pagamento.objects.all()

    if request.method == 'POST':
        pagamento_id = request.POST.get('id_pagamento')
        novo_status = request.POST.get('status_pagamento')
        novo_metodo = request.POST.get('metodo_de_pagamento')

        pagamento = Pagamento.objects.get(id_pagamento=pagamento_id)
        pagamento.status_pagamento = novo_status
        pagamento.metodo_de_pagamento = novo_metodo
        pagamento.save(update_fields=['status_pagamento', 'metodo_de_pagamento'])

        return redirect('editar_pagamentos')

    return render(request, 'vendas/editar_pagamentos.html', {'pagamentos': pagamentos})
