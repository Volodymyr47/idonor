from django.urls import path
from donor import views


urlpatterns = [
    path('', views.home, name='home'),
    path('info/<int:profile_id>/', views.donor_info, name='donor_info'),
    path('history/<int:profile_id>/', views.get_history, name='get_history'),
    path('test/', views.take_test, name='make_test'),
    path('save-answer/', views.save_test_answer, name='save_test_answer'),
    path('result/', views.get_result, name='get_result'),
]