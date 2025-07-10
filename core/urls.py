# core/urls.py
from django.urls import include, path
from django.contrib.auth import views as auth_views # Importe as views de autenticação
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
import core.views as views

app_name = 'core'

urlpatterns = [
    path('clientes/', views.ClienteViewSet.as_view({'get': 'list'}), name='clientes'),
    
]