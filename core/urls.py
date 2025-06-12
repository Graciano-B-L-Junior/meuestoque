# core/urls.py
from django.urls import path
from .views import lista_produtos, detalhe_produto, adicionar_produto, editar_produto, deletar_produto

app_name = 'core'

urlpatterns = [
    path('', lista_produtos, name='lista_produtos'),
    path('produto/<int:pk>/', detalhe_produto, name='detalhe_produto'),
    path('produto/adicionar/', adicionar_produto, name='adicionar_produto'),
    path('produto/editar/<int:pk>/', editar_produto, name='editar_produto'),
    path('produto/deletar/<int:pk>/', deletar_produto, name='deletar_produto'),
]