from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('refresh_wallet_info', views.refresh_wallet_info, name='refresh_wallet_info'),
    # path('generate_new_address', views.generate_new_address, name='generate_new_address'),
    path('logout', views.logout, name='logout'),
]
