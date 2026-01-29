from django.urls import path
from . import views


app_name = 'website'


urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/buy/', views.buy_crypto, name='buy'),
    path('dashboard/sell/', views.sell_crypto, name='sell'),

    path('privacy_policy/', views.privacy_policy, name="privacy_policy"),
    path('terms-of-use/', views.terms_of_use, name="terms_of_use"),
    # urls.py
    path("dashboard/load-more/", views.load_more_purchases, name="load_more_purchases"),
    path("dashboard/load-more-sells/", views.load_more_sell_transactions, name="load_more_sell_transactions"),
    path("settings/", views.account_settings, name="account_settings"),
    


]