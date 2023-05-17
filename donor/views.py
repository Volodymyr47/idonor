import logging
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model


import config
import constant as con
from .donor_utils import sort_answer_in_dict
from .models import Profile, History, Test, TestDetail
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
        categories = QuestionCategory.objects.filter(id__in=categories_id).order_by('id')
    except Exception as err:
        messages.error(request, 'Questions or Categories selection error')
        logging.error(f'Questions or Categories selection error:\n{err}')

    per_page = 4
    paginator = Paginator(categories, per_page=per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'donor/test.html', {'questions': questions,
                                               'categories': page_obj,
                                               'instruction_title': con.TEST_INSTRUCTION_TITLE,
                                               'instruction_text': con.TEST_INSTRUCTION_TEXT})


def save_test_result(request):
    """
    Save donor test result and redirect to home-page
    """
    if request.method == 'POST':
        user = request.user
        pre_test_result = {key[7:]: value for key, value in request.POST.items() if key.startswith('answer')
                           or key.startswith('answer_text')}

        test_result = sort_answer_in_dict(pre_test_result, 5)

        try:
            test = Test.objects.create(profile_id=30)
            test.save()
            for key, value in test_result.items():
                test_detail = TestDetail.objects.create(test_id=test.pk,
                                                        question_id=int(key),
                                                        answer=value)
        except Exception as err:
            logging.error(f'Test saving error:\n{err}')
            messages.error('Помилка збереження результатів анкети')

        print(test_result)

    return redirect('take_test')


def get_test_result(request):
    pass
