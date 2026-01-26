from django.urls import path
from . import views




app_name = 'users'


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('password_change/', views.password_change_view, name='password_change'),
    path('password_change/done/', views.password_change_done_view, name='password_change_done'),
    #path('dashboard/', views.dashboard, name='dashboard'),  # example dashboard
]