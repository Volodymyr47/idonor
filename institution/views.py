import logging
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

import config
from .models import Question, QuestionCategory, Institution
from donor.models import (Profile,
                          Test,
                          TestDetail,
                          Status,
                          BloodParameter,
                          CurrentHealthParameter)

User = get_user_model()


def main_page(request):
    """
    Show main page of the institution
    :param request:
    :return:
    """
    return render(request, 'institution/main.html')


def get_institution_info(request):
    """
    Get information about the institution
    :param request:
    :return:
    """
    all_data = None
    try:
        all_data = Institution.objects.filter(full_name__icontains='Сокаль'
                                              ).first()
    except Exception as err:
        logging.error(f'Selecting all data at "get_institution_info" error occurred\n{err}')
        messages.error(request, 'Selecting all data at "get_institution_info" error occurred')
    return render(request, 'institution/institution.html', {'all_data': all_data})


def get_all_donors(request):
    try:
        donors = Profile.objects.filter(test__profile_id__isnull=False,
                                        ).values('test__status', 'user__username', 'id'
                                                 ).distinct().order_by('test__status', 'user__username')

    except Exception as err:
        logging.error(f'Function "get all donors" error occurred:\n{err}')
        messages.error(request, 'Помилка отримання переліку донорів')
        return redirect('get_all_donors')

    return render(request, 'institution/donors.html', {'donors': donors})


def specific_donor(request, donor_id):
    try:
        donor = Profile.objects.get(id=donor_id)
        tests = Test.objects.filter(profile_id=donor_id).all().order_by('-test_date')
        statuses = Status.objects.filter(code__lte=9).all()
    except Exception as err:
        logging.error(f'Function "specific_donor" error occurred:\n{err}')
        messages.error(request, 'Помилка отримання інформації про донора')
        return redirect('specific_donor', donor_id)
    return render(request, 'institution/specific_donor.html', {'donor': donor,
                                                               'tests': tests,
                                                               'statuses': statuses})


def edit_donor(request, donor_id):
    if request.method == 'POST':
        status = request.POST.get('new_status')
        try:
            new_status = Status.objects.get(code=status)
            donor_profile = Profile.objects.get(id=donor_id)
            donor_profile.status = new_status
            donor_profile.save()
            return redirect('specific_donor', donor_id)
        except Exception as err:
            logging.error(f'Function "edit_donor" error occurred:\n{err}')
            messages.error(request, 'Помилка редагування інформації про донора')
            return redirect('edit_donor', donor_id)
    return redirect('all_donors')


def get_donor_test_result(request, donor_id, to_date):
    try:
        test = Test.objects.filter(profile_id=donor_id,
                                   test_date=to_date).first()

        new_test_status = Status.objects.get(code=12)
        test.status = new_test_status
        test.save()

        test_details = TestDetail.objects.filter(test_id=test.pk).all()
    except Exception as err:
        messages.error(request, 'Помилка отримання даних з тестів')
        logging.error(f'Function "get_donor_test_result" error occurred:\n{err}')
        return redirect(get_donor_test_result, donor_id, to_date)

    return render(request, 'institution/donor-test-result.html', {'test': test,
                                                                  'test_details': test_details})


def health_parameter(request, donor_id):
    if request.method == 'POST':
        blood_type = request.POST.get('blood_type')
        rh_factor = request.POST.get('rh_factor')
        common_info = request.POST.get('common_info')

        if blood_type or rh_factor or common_info:
            blood_param = BloodParameter.objects.create(profile=donor_id,
                                                        blood_type=blood_type,
                                                        rh_factor=rh_factor,
                                                        common_info=common_info
                                                        )
       #Дописати додавання поточних параметрів тиску, і т.д
        return redirect('specific_donor.html', donor_id)


def all_categories(request):
    """
    Create a category and show all the categories existing
    :param request: request
    :return: page of questions
    """
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        if category_name:
            try:
                institution = Institution.objects.filter(
                    full_name__icontains=config.INSTITUTION_CITY
                ).values('full_name').first()

                add_category = QuestionCategory(name=category_name.upper(),
                                                institution_id=institution.pk)
                add_category.save()
            except Exception as err:
                messages.error(request, 'Adding new category error occurred')
                logging.error(f'Adding new category at "get_all_categories" error occurred\n{err}')
        else:
            messages.error(request, 'The field of "category name" must be populated')
    categories = QuestionCategory.objects.all().order_by('dlm')
    per_page = 10
    paginator = Paginator(categories, per_page=per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'institution/categories.html', {'categories': page_obj})


def edit_category(request, category_id):
    """
    Edit the category with id = category_id
    :param request: request
    :param category_id: int - category_id id
    :return: current page
    """
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        if new_name is None:
            messages.error(request, f'Editing category at "edit_category with id {category_id}" error occurred')
            return redirect('all_categories')
        try:
            edited_category = QuestionCategory.objects.filter(id=category_id).get()
            edited_category.name = new_name
            edited_category.save()
        except Exception as err:
            logging.error(f'Editing category at "edit_category with id {category_id}" error occurred\n{err}')
            return redirect('all_categories')

    return redirect('all_categories', permanent=True)


def delete_category(request, category_id):
    """
     Delete the category with id = category_id
     :param request: request
     :param category_id: int - category_id id
     :return: current page
     """
    try:
        edited_category = QuestionCategory.objects.get(id=category_id)
        edited_category.delete()
    except Exception as err:

        messages.error(request, f'Deleting category at "delete_category with id {category_id}" error occurred')
        logging.error(f'Deleting category at "delete_category with id {category_id}" error occurred\n{err}')
        return redirect('all_categories')
    return redirect('all_categories', permanent=True)


def all_questions(request):
    """
    Create a question and show all the questions existing
    :param request:
    :return: page of questions
    """
    if request.method == 'POST':
        question_text = request.POST.get('question')
        category = request.POST.get('category')
        if question_text:
            try:
                add_question = Question(text=question_text,
                                        category_id=category)
                add_question.save()
            except Exception as err:
                logging.error(f'Adding new question at "get_all_questions" error occurred\n{err}')
        else:
            messages.error(request, 'The field of "question text" must be populated')

    categories = None
    questions = None
    categories_list = None

    try:
        questions = Question.objects.all().order_by('dlm')
        categories_id = []
        for question in questions:
            categories_id.append(question.category_id)
        categories = QuestionCategory.objects.filter(id__in=categories_id).order_by('id')
        categories_list = QuestionCategory.objects.all().order_by('id')
    except Exception as err:
        messages.error(request, 'Questions or Categories selection error')
        logging.error(f'Questions or Categories selection error:\n{err}')

    per_page = 4
    paginator = Paginator(categories, per_page=per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    previous_page = request.POST.get('previous')
    if previous_page:
        redirect(previous_page)

    return render(request, 'institution/questions.html', {'questions': questions,
                                                          'categories': page_obj,
                                                          'categories_list': categories_list})


def edit_question(request, question_id):
    """
    Edit the question with id = question_id
    :param request: request
    :param question_id: int - question id
    :return: current page
    """
    if request.method == 'POST':
        new_text = request.POST.get('text')
        if new_text is None:
            messages.error(request, f'Editing question at "edit_question" with id {question_id}" error occurred')
            return redirect('all_questions')
        try:
            edited_question = Question.objects.filter(id=question_id).get()
            edited_question.text = new_text
            edited_question.save()
        except Exception as err:
            logging.error(f'Adding new question at "edit_question with id {question_id}" error occurred\n{err}')

    return redirect('all_questions', permanent=True)


def delete_question(request, question_id):
    """
    Delete the question with id = question_id
    :param request: request
    :param question_id: int - question id
    :return: current page
    """
    try:
        question = Question.objects.filter(id=question_id).first()
        question.delete()
    except Exception as err:
        messages.error(request, f'Deleting question at "delete_question with id {question_id}" error occurred')
        logging.error(f'Deleting question at "delete_question with id {question_id}" error occurred\n{err}')
        return redirect('all_questions')

    return redirect('all_questions', permanent=True)
