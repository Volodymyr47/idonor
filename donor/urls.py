from django.urls import path
from donor import views


urlpatterns = [
    path('', views.home, name='home'),
    path('user-info/', views.user_info, name='user_info'),
    path('test/', views.take_test, name='make_test'),
    path('save-answer/', views.save_test_answer, name='save_test_answer'),
    path('result/', views.get_result, name='get_result'),
]