from django.urls import path
from . import views


app_name = 'website'


urlpatterns = [
path('', views.index, name='index'),
path('dashboard/', views.dashboard, name='dashboard'),
path('dashboard/buy/', views.buy_crypto, name='buy'),
path("coinbase/callback/", views.coinbase_callback, name="coinbase_callback"),
path('dashboard/sell/', views.sell_crypto, name='sell'),
path('dashboard/withdraw/', views.withdraw_crypto, name='withdraw'),
path('privacy_policy/', views.privacy_policy, name="privacy_policy"),
path('terms-of-use/', views.terms_of_use, name="terms_of_use"),
]