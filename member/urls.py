from django.urls import path
from member import views


app_name = 'member'
urlpatterns = [
    path('api/member', views.main),
]