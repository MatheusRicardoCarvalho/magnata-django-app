from django.urls import path
from . import views

urlpatterns = [
        path('wallet/', views.wallet , name='wallet'),
        path('login/', views.login_view, name='login'),
        path('register/', views.register_view, name='register'),
        path('logout/', views.logout_view, name='logout'),
        path('wallet/wallet_management', views.wallet_management, name='wallet_management'),
        path('wallet/buy_stock', views.buy_stock, name='buy_stock'),
        path('wallet/create_wallet', views.create_wallet, name='create_wallet'),
        path('', views.home, name='home'), 
        path('wallet/add_stock', views.add_stock, name='add_stock'),
        path('wallet/sell_stock', views.sell_stock, name='sell_stock'),

]
