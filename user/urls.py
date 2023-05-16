from django.urls import path
from user import views


urlpatterns = [
    path('registration/', views.register, name='register'),
    path('login/', views.make_login, name='make_login'),
    path('logout/', views.user_logout, name='logout'),
    path('password-recover/', views.recover_password, name='recover_password'),
    path('password-sent/', views.password_sent, name='password_sent'),
    path('password-change/<slug:uidb64>/<slug:token>/', views.change_password, name='change_password'),
    path('info/<int:user_id>/', views.get_user_info, name='user_info'),
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
]
