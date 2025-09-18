from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('orders/', views.orders, name='accounts.orders'),
    path('settings/', views.settings, name='accounts.settings'),
    path('forgot-password/', views.forgot_password, name='accounts.forgot_password'),
    path('security-question/', views.security_question, name='accounts.security_question'),
    path('reset-password/', views.reset_password, name='accounts.reset_password'),
]