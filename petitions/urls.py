from django.urls import path
from . import views

urlpatterns = [
    path('', views.petition_list, name='petitions.index'),
    path('create/', views.petition_create, name='petitions.create'),
    path('<int:petition_id>/', views.petition_detail, name='petitions.detail'),
    path('<int:petition_id>/vote/', views.petition_vote, name='petitions.vote'),
    path('my-petitions/', views.my_petitions, name='petitions.my_petitions'),
]

