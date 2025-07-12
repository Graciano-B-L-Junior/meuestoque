

from rest_framework import serializers
from .models import Movimentacao, Produto

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'estoque_usuario', 'nome', 'preco_custo', 'preco_venda']


class MovimentacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimentacao
        fields = ['id', 'produto', 'quantidade', 'tipo_movimentacao', 'descricao', 'data_movimentacao']
