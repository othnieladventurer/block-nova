from django.urls import path
from . import views


app_name = 'website'


urlpatterns = [
path('', views.index, name='index'),
path('dashboard/', views.dashboard, name='dashboard'),
path('dashboard/buy/', views.buy_crypto, name='buy'),
path('dashboard/sell/', views.sell_crypto, name='sell'),
path('dashboard/withdraw/', views.withdraw_crypto, name='withdraw'),
]