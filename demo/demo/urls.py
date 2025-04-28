"""
URL configuration for demo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    path('clientes', views.gerenciar_clientes, name='gerenciar_clientes'),
]

