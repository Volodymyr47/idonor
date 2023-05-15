from django.urls import path, include
from user import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('registration/', views.register, name='register'),
    path('login/', views.pre_login, name='pre_login'),
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
]
