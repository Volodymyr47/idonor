from django.urls import path
from institution import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('donors/', views.get_all_donors, name='all_donors'),
    path('categories/', views.all_categories, name='all_categories'),
    path('category/<int:category_id>/edit/', views.edit_category, name='edit_category'),
    path('category/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('questions/', views.all_questions, name='all_questions'),
    path('question/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('question/<int:question_id>/delete/', views.delete_question, name='delete_question'),
]