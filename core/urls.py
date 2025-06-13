# core/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views # Importe as views de autenticação
from .views import (
    lista_produtos,
    detalhe_produto,
    adicionar_produto,
    editar_produto,
    deletar_produto,
    registrar,
    adicionar_movimento # Importe a nova view de registro
)

app_name = 'core'

urlpatterns = [
    # URLs de Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:login'), name='logout'),
    path('registrar/', registrar, name='registrar'),

    # URLs do Estoque
    path('', lista_produtos, name='lista_produtos'),
    path('produto/<int:pk>/', detalhe_produto, name='detalhe_produto'),
    path('produto/adicionar/', adicionar_produto, name='adicionar_produto'),
    path('produto/editar/<int:pk>/', editar_produto, name='editar_produto'),
    path('produto/deletar/<int:pk>/', deletar_produto, name='deletar_produto'),
    # Nova URL para registrar movimentação
    path('produto/<int:produto_pk>/movimentar/', adicionar_movimento, name='adicionar_movimento'),
]