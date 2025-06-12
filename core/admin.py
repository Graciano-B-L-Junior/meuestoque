# core/admin.py
from django.contrib import admin
from .models import Produto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco_venda', 'quantidade', 'data_atualizacao')
    search_fields = ('nome',)
    list_filter = ('data_criacao',)