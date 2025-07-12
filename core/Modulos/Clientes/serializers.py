
from rest_framework import serializers
from .models import Cliente, OrdemDeServico, ItemCliente

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'cliente_de_user', 'nome', 'sobrenome', 'celular', 'email', 'data_cadastro']

class OrdemDeServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdemDeServico
        fields = ['id', 'cliente', 'situacao', 'data_inicio', 'data_termino', 'item_do_cliente']

class ItemClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCliente
        fields = ['id', 'veiculo', 'cliente']

