from django.urls import path
from order import views


app_name = 'order'
urlpatterns = [
    path('booking/', views.main),
    path('api/book', views.book),
    path('api/order', views.order),
]


