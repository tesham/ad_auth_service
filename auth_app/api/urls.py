from django.urls import path
from . import view

urlpatterns = [
    path('token', view.GenerateJwtTokenApiView.as_view(), name='generate_token_api_view'),
    path('token/refresh', view.RefreshTokenApiView.as_view(), name='refresh_token_api_view'),
    path('logout', view.LogoutView.as_view(), name='logout_api_view')
]