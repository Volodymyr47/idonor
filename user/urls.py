from django.urls import path
from user import views


urlpatterns = [
    path('registration/', views.register, name='register'),
    path('login/', views.make_login, name='make_login'),
    path('logout/', views.user_logout, name='logout'),
    path('prepare_password_recover/', views.prepare_password_recover, name='prepare_password_recover'),
    path('password-sent/', views.password_sent, name='password_sent'),
    path('recover_password/<slug:uidb64>/<slug:token>/',views.recover_password, name='recover_password'),
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),

]
