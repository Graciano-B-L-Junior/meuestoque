# core/admin.py
from django.contrib import admin
from .models import MovimentoEstoque, Produto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # Adicionamos os campos e as propriedades calculadas
    list_display = (
        'nome', 
        'preco_compra', 
        'preco_venda', 
        'quantidade', 
        'valor_total_estoque', # Adicionado aqui
        'lucro', 
        'porcentagem_lucro_formatada', 
        'data_atualizacao'
    )
    search_fields = ('nome',)
    list_filter = ('usuario', 'data_criacao',) # Adicionamos o filtro por usuário
    
    # Criamos um método para formatar a porcentagem no admin
    def porcentagem_lucro_formatada(self, obj):
        return f"{obj.porcentagem_lucro:.2f}%"
    porcentagem_lucro_formatada.short_description = 'Margem de Lucro (%)'

@admin.register(MovimentoEstoque)
class MovimentoEstoqueAdmin(admin.ModelAdmin):
    list_display = ('produto', 'tipo_movimento', 'quantidade', 'data_movimentacao', 'observacao')
    list_filter = ('produto', 'tipo_movimento', 'data_movimentacao')
    search_fields = ('produto__nome', 'observacao')