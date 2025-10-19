from django.urls import path
from . import views

urlpatterns = [
    path('trending-map/', views.TrendingMapView.as_view(), name='trending_map'),
    path('api/trending-data/', views.trending_data_api, name='trending_data_api'),
    path('api/region/<int:region_id>/trending/', views.region_trending_api, name='region_trending_api'),
    path('api/set-user-region/', views.set_user_region_api, name='set_user_region_api'),
    path('api/user-region/', views.user_region_api, name='user_region_api'),
]
