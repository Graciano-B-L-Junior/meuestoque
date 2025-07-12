# users/urls.py
from django.urls import path

from core.Modulos.Estoque import views
from .views import UserListView, UserRegisterView
from core.Modulos.Estoque import views as estoque_views
from core.Modulos.Financeiro import views as financeiro_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'core'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   # login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # refresh
]

urlpatterns += [
    path('produtos/', views.ProdutoList.as_view(), name='produto-list'),
    path('produtos/<int:pk>/', views.ProdutoDetail.as_view(), name='produto-detail'),
    path('movimentos/', views.MovimentacaoList.as_view(), name='movimento-list'),
    path('movimentos/<int:pk>/', views.MovimentacaoDetail.as_view(), name='movimento-detail'),
]

urlpatterns += [
    path('estoque/produtos/', estoque_views.ProdutoList.as_view(), name='estoque-produto-list'),
    path('estoque/produtos/<int:pk>/', estoque_views.ProdutoDetail.as_view(), name='estoque-produto-detail'),
    path('estoque/movimentos/', estoque_views.MovimentacaoList.as_view(), name='estoque-movimento-list'),
    path('estoque/movimentos/<int:pk>/', estoque_views.MovimentacaoDetail.as_view(), name='estoque-movimento-detail'),
]

urlpatterns += [
    path('financeiro/pagamentos/', financeiro_views.PagamentoListCreateView.as_view(), name='financeiro-pagamento-list'),
    path('financeiro/pagamentos/<int:pk>/', financeiro_views.PagamentoDetail.as_view(), name='financeiro-pagamento-detail'),
]


