
from rest_framework import viewsets
from .models import Cliente, ItemCliente, OrdemDeServico
from .serializers import ClienteSerializer, ItemClienteSerializer, OrdemDeServicoSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ItemClienteViewSet(viewsets.ModelViewSet):
    queryset = ItemCliente.objects.all()
    serializer_class = ItemClienteSerializer


class OrdemDeServicoViewSet(viewsets.ModelViewSet):
    queryset = OrdemDeServico.objects.all()
    serializer_class = OrdemDeServicoSerializer
