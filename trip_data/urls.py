from django.urls import path
from trip_data import views


app_name = 'trip_data'
urlpatterns = [
    path('', views.main),

    path('api/trip_data/page=<int:num>/keyword=<str:keyword>', views.trip_data),

    path('attraction/<int:num>', views.attraction_web),
    path('api/attraction/<int:num>', views.attraction),
]