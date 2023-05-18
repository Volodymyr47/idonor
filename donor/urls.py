from django.urls import path
from donor import views


urlpatterns = [
    path('', views.home, name='home'),
    path('info/<int:profile_id>/', views.donor_info, name='donor_info'),
    path('history/<int:profile_id>/', views.get_history, name='get_history'),
    path('test/', views.take_test, name='take_test'),
    path('save-test-result/', views.save_test_result, name='save_test_result'),
    path('test-result/<int:user_id>/', views.get_test_result, name='get_test_result'),
    path('test-passed/', views.test_passed, name='test_passed'),
]