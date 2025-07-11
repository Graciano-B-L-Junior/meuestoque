# users/urls.py
from django.urls import path

from core.Estoque import views
from .views import UserListView, UserRegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   # login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # refresh

    #===== Estoque ======== #
    path('produtos/', views.ProdutoList.as_view(), name='produto-list'),
    path('produtos/<int:pk>/', views.ProdutoDetail.as_view(), name='produto-detail'),
    path('movimentos/', views.MovimentacaoList.as_view(), name='movimento-list'),
    path('movimentos/<int:pk>/', views.MovimentacaoDetail.as_view(), name='movimento-detail'),
]
