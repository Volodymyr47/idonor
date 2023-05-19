from django.urls import path
from institution import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('info/', views.get_institution_info, name='get_institution_info'),
    path('donors/', views.get_all_donors, name='all_donors'),
    path('donor/<int:donor_id>/', views.specific_donor, name='specific_donor'),
    path('donor/<int:donor_id>/edit/', views.change_donor_status, name='change_donor_status'),
    path('donor/<int:donor_id>/blood-params/add/', views.add_blood_params, name='add_blood_params'),
    path('donor/<int:donor_id>/blood-params/edit/', views.edit_blood_params, name='edit_blood_params'),
    path('donor/<int:donor_id>/test-result/<str:to_date>/', views.get_donor_test_result, name='donor_test_result'),
    path('donor/<int:donor_id>/history/', views.donor_history, name='donor_history'),
    path('donor/<int:donor_id>/history/<int:history_id>/edit/', views.edit_donor_history, name='edit_donor_history'),
    path('categories/', views.all_categories, name='all_categories'),
    path('category/<int:category_id>/edit/', views.edit_category, name='edit_category'),
    path('category/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('questions/', views.all_questions, name='all_questions'),
    path('question/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('delete-question/<int:question_id>/', views.delete_question, name='delete_question'),
]