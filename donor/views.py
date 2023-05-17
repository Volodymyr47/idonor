import logging
from django.contrib import messages
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from .models import Profile, History, Test

import config
from institution.models import Institution, Question, QuestionCategory

User = get_user_model()


def home(request):
    inst_name = None
    try:
        inst_name = Institution.objects.filter(
            full_name__icontains=config.INSTITUTION_CITY
        ).values('full_name').first()

    except Exception as err:
        logging.error(f"Home func error:\n{err}")
        messages.error(request, 'Home func error occurred!')
    return render(request, 'donor/home.html', {'inst_name': inst_name})


def donor_info(request, profile_id):
    profile_info = None
    try:
        profile_info = Profile.objects.filter(id=profile_id).all()

    except Exception as err:
        logging.error(f'Function "Get_user_info" error: \n{err}')

    return render(request, 'donor/donor-info.html', {'profile_info': profile_info})


def get_history(request, profile_id):
    history = None
    try:
        history = History.objects.filter(profile_id=profile_id).all().order_by('-donation_date')
    except Exception as err:
        logging.error(f'Function "Get_history" error: \n{err}')

    per_page = 6
    paginator = Paginator(history, per_page)
    page_number = request.GET.get('page')
    history_page = paginator.get_page(page_number)

    return render(request, 'donor/history.html', {'history': history_page})


def take_test(request):
    categories = None
    questions = None

    try:
        questions = Question.objects.all().order_by('dlm')
        categories_id = []
        for question in questions:
            categories_id.append(question.category_id)
        categories = QuestionCategory.objects.filter(id__in=categories_id).order_by('name')
    except Exception as err:
        messages.error(request, 'Questions or Categories selection error')
        logging.error(f'Questions or Categories selection error:\n{err}')

    per_page = 4
    paginator = Paginator(categories, per_page=per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'donor/test.html', {'questions': questions,
                                               'categories': page_obj})


def save_test_result(request):
    pass


def get_test_result(request):
    pass
