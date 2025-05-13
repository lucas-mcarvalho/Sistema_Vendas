
from django.contrib import admin
from django.urls import path, include
from vendas import views

urlpatterns = [
    path('cadastro-cliente/', views.cadastro_cliente, name='cadastro_cliente'),
    path('novo-fornecedor/', views.criar_novo_fornecedor, name='criar_novo_fornecedor'),
    path('novo-produto/', views.criar_registro_do_produto, name='criar_registro_do_produto'),
    path('novo-pedido/', views.registrar_novo_pedido, name='registrar_novo_pedido'),
    path('verificar-pagamento/<int:id_pedido>/', views.verificar_pagamento, name='verificar_pagamento'),
    path('adicionar-itens/<int:id_pedido>/', views.adicionar_itens, name='adicionar_itens'),
    path('olhar_tabelas', views.olhar_tabelas, name='olhar_tabelas'),
    path('ver_clientes', views.ver_clientes, name='ver_clientes'),
    path('ver_pedidos', views.ver_pedidos, name='ver_pedidos'),
    path('ver_fornecedores', views.ver_fornecedores, name='ver_fornecedores'),
    path('ver_produtos', views.ver_produtos, name='ver_produtos'),
    path('', views.index, name='index'),
    path('gerenciar_clientes', views.gerenciar_clientes, name='gerenciar_clientes'),
    path('ver_fornecedores/editar/<int:id>', views.editar_fornecedor, name='editar_fornecedor'),
    path('ver_produtos/editar/<int:id>', views.editar_produtos, name='editar_produtos'),
    path('editar_cliente/editar/<int:id_cliente>/', views.editar_cliente, name='editar_cliente'),
    path('pedidos/acao/<int:id_pedido>/', views.escolher_acao_pedido, name='escolher_acao_pedido'),
    path('pedidos/editar/<int:id>/', views.editar_pedido, name='editar_pedido'),
    path('pagamentos/', views.editar_pagamentos, name='editar_pagamentos'), 
]

