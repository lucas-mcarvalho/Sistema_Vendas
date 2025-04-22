from django.urls import path
from . import views

urlpatterns = [
    path('cadastro-cliente/', views.cadastro_cliente, name='cadastro_cliente'),
    path('novo-fornecedor/', views.criar_novo_fornecedor, name='criar_novo_fornecedor'),
    path('novo-produto/', views.criar_registro_do_produto, name='criar_registro_do_produto'),
    path('novo-pedido/', views.registrar_novo_pedido, name='registrar_novo_pedido'),
    path('verificar-pagamento/<int:id_pedido>/', views.verificar_pagamento, name='verificar_pagamento'),
    path('adicionar-itens/<int:id_pedido>/', views.adicionar_itens, name='adicionar_itens'),
    path('', views.index, name='index'),
]
