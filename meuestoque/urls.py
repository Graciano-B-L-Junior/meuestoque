# gestao_estoque/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')), # Inclui as URLs do app core
]