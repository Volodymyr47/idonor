from django.urls import path
from donor import views

urlpatterns = [
    path('', views.home, name='home'),
]