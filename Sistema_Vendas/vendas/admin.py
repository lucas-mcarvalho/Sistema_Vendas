from django.contrib import admin
from .models import Cliente, Pedido, Fornecedor, Produto, Pagamento, Itens_Pedido
# Register your models here.

admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(Fornecedor)
admin.site.register(Produto)
admin.site.register(Pagamento)
admin.site.register(Itens_Pedido)