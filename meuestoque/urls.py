# gestao_estoque/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from core import views

# router = routers.DefaultRouter()
# router.register(r'produtos', views.ProdutoViewSet)
# router.register(r'movimentos', views.MovimentoEstoqueViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('core.urls', namespace='core')), # Inclui as URLs do app core
    path('api/', include('core.urls')),

    path('api-auth/', include('rest_framework.urls')),
    
]