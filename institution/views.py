import logging
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

import config
from user.utils import specialist_required
from .models import Question, QuestionCategory, Institution
from donor.models import (Profile,
                          Test,
                          TestDetail,
                          Status,
                          History,
                          BloodParameter,
                          CurrentHealthParameter)

User = get_user_model()


@login_required(login_url='/user/login')
@specialist_required
def main_page(request):
    """
    Show main page of the institution
    :param request:
    :return:
    """
    institution = Institution.objects.filter(full_name__icontains=config.INSTITUTION_CITY).first()
    return render(request, 'institution/main.html', {'institution': institution})


@login_required(login_url='/user/login')
@specialist_required
def get_institution_info(request):
    """
    Get information about the institution
    :param request:
    :return:
    """
    all_data = None
    try:
        all_data = Institution.objects.filter(full_name__icontains=config.INSTITUTION_CITY
                                              ).first()
    except Exception as err:
        logging.error(f'Selecting all data at "get_institution_info" error occurred\n{err}')
        messages.error(request, 'Selecting all data at "get_institution_info" error occurred')
    return render(request, 'institution/institution.html', {'all_data': all_data})


@login_required(login_url='/user/login')
@specialist_required
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


@login_required(login_url='/user/login')
@specialist_required
def specific_donor(request, donor_id):
    try:
        donor = Profile.objects.get(id=donor_id)
        tests = Test.objects.filter(profile_id=donor_id).all().order_by('-test_date')
        statuses = Status.objects.filter(code__lte=9).all()
        resuses = BloodParameter.Rh_FACTOR
    except Exception as err:
        logging.error(f'Function "specific_donor" error occurred:\n{err}')
        messages.error(request, 'Помилка отримання інформації про донора')
        return redirect('specific_donor', donor_id)
    return render(request, 'institution/specific_donor.html', {'donor': donor,
                                                               'tests': tests,
                                                               'statuses': statuses,
                                                               'resuses': resuses})


@login_required(login_url='/user/login')
@specialist_required
def change_donor_status(request, donor_id):
    if request.method == 'POST':
        status = request.POST.get('new_status')
        try:
            new_status = Status.objects.get(code=status)
            donor_profile = Profile.objects.get(id=donor_id)
            donor_profile.status = new_status
            donor_profile.save()
            return redirect('specific_donor', donor_id)
        except Exception as err:
            logging.error(f'Function "change_donor_status" error occurred:\n{err}')
            messages.error(request, 'Помилка редагування інформації про донора')
            return redirect('specific_donor', donor_id)
    return redirect('all_donors')


@login_required(login_url='/user/login')
@specialist_required
def get_donor_test_result(request, donor_id, to_date):
    try:
        test = Test.objects.filter(profile_id=donor_id,
                                   test_date=to_date).first()

        new_test_status = Status.objects.get(code=12)
        test.status = new_test_status
        test.save()

        test_details = TestDetail.objects.filter(test_id=test.pk).all()
    except Exception as err:
        logging.error(f'Function "get_donor_test_result" error occurred:\n{err}')
        messages.error(request, 'Помилка отримання даних з тестів')
        return redirect('get_donor_test_result', donor_id, to_date)

    return render(request, 'institution/donor-test-result.html', {'test': test,
                                                                  'test_details': test_details})


@login_required(login_url='/user/login')
@specialist_required
def donor_history(request, donor_id):
    if request.method == 'POST':
        create_history = None

        donation_date = request.POST.get('donation_date')
        donated_volume = request.POST.get('donated_volume')

        heart_rate = request.POST.get('heart_rate')
        hemoglobin = request.POST.get('hemoglobin')
        blood_pressure = request.POST.get('blood_pressure')
        comment = request.POST.get('comment')

        try:
            if donation_date or donated_volume:
                donor_profile = Profile.objects.get(id=donor_id)
                create_history = History.objects.create(profile=donor_profile,
                                                        donation_date=donation_date,
                                                        donated_volume=donated_volume)

            if heart_rate or hemoglobin or blood_pressure or comment:
                create_healthparam = CurrentHealthParameter.objects.create(history=create_history,
                                                                           blood_pressure=blood_pressure,
                                                                           heart_rate=heart_rate,
                                                                           hemoglobin=hemoglobin,
                                                                           common_info=comment)
            return redirect('donor_history', donor_id)
        except Exception as err:
            logging.error(f'Function "add_donor_history" error occurred:\n{err}')
            messages.error(request, 'Помилка додавання донорської історії')
            return redirect('show_donor_history', donor_id)
    try:
        history = History.objects.filter(profile=donor_id).all().order_by('-donation_date')
    except Exception as err:
        logging.error(f'Function "add_donor_history" error occurred:\n{err}')
        messages.error(request, 'Помилка отримання донорської історії')
        return redirect('donor_history', donor_id)

    per_page = 2
    paginator = Paginator(history, per_page=per_page)
    page_number = request.GET.get('page')
    history_page = paginator.get_page(page_number)

    return render(request, 'institution/donor-history.html', {'history': history_page,
                                                              'donor_id': donor_id})


@login_required(login_url='/user/login')
@specialist_required
def edit_donor_history(request, donor_id, history_id):
    if request.method == 'POST':

        donation_date = request.POST.get('ed_donation_date')
        donated_volume = request.POST.get('ed_donated_volume')
        comment = request.POST.get('ed_comment')

        heart_rate = request.POST.get('ed_heart_rate')
        hemoglobin = request.POST.get('ed_hemoglobin')
        blood_pressure = request.POST.get('ed_blood_pressure')
        common_info = request.POST.get('ed_common_info')

        try:
            edit_history = History.objects.get(id=history_id,
                                               profile_id=donor_id)
            edit_history.donation_date = donation_date
            edit_history.donated_volume = donated_volume
            edit_history.comment = comment
            edit_history.save()

            edit_health_param = CurrentHealthParameter.objects.get(history_id=history_id)
            edit_health_param.blood_pressure = blood_pressure
            edit_health_param.heart_rate = heart_rate
            edit_health_param.hemoglobin = hemoglobin
            edit_health_param.common_info = common_info
            edit_health_param.save()

            return redirect('donor_history', donor_id)
        except Exception as err:
            logging.error(f'Function "edit_donor_history" error occurred:\n{err}')
            messages.error(request, 'Помилка редагування донорської історії')
            return redirect('donor_history', donor_id)
    return redirect('donor_history', donor_id)


@login_required(login_url='/user/login')
@specialist_required
def add_blood_params(request, donor_id):
    """
    Add blood params
    :param request: request
    :param donor_id: int - donor's id (profile.id)
    :return:
    """
    if request.method == 'POST':
        blood_type = request.POST.get('blood_type')
        rh_factor = request.POST.get('rh_factor')
        common_info = request.POST.get('common_info')

        if blood_type or rh_factor or common_info:
            try:
                profile = Profile.objects.get(id=donor_id)

                blood_param = BloodParameter.objects.create(profile=profile,
                                                            blood_type=blood_type,
                                                            rh_factor=rh_factor,
                                                            common_info=common_info
                                                            )
            except Exception as err:
                messages.error(request, 'Помилка додавання інформації про кров')
                logging.error(f'Function "add_blood_params" error occurred:\n{err}')
                return redirect('specific_donor', donor_id)
    return redirect('specific_donor', donor_id)


@login_required(login_url='/user/login')
@specialist_required
def edit_blood_params(request, donor_id):
    """
    Edit blood params
    :param request: request
    :param donor_id: int - donor's id (profile.id)
    :return:
    """
    if request.method == 'POST':
        blood_type = request.POST.get('blood_type')
        rh_factor = request.POST.get('rh_factor')
        common_info = request.POST.get('common_info')

        if blood_type or rh_factor or common_info:
            try:
                blood_param = BloodParameter.objects.filter(profile_id=donor_id).first()
                blood_param.blood_type = blood_type
                blood_param.rh_factor = rh_factor
                blood_param.common_info = common_info
                blood_param.save()
            except Exception as err:
                messages.error(request, 'Помилка редагування інформації по крові')
                logging.error(f'Function "edit_blood_params" error occurred:\n{err}')
                return redirect('specific_donor', donor_id)
    return redirect('specific_donor', donor_id)


@login_required(login_url='/user/login')
@specialist_required
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
                ).first()

                add_category = QuestionCategory.objects.create(name=category_name.upper(),
                                                               institution_id=institution.pk)
            except Exception as err:
                messages.error(request, 'Adding new category error occurred')
                logging.error(f'Adding new category at "all_categories" error occurred\n{err}')
        else:
            messages.error(request, 'The field of "category name" must be populated')
    categories = QuestionCategory.objects.all().order_by('dlm')
    per_page = 10
    paginator = Paginator(categories, per_page=per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'institution/categories.html', {'categories': page_obj})


@login_required(login_url='/user/login')
@specialist_required
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


@login_required(login_url='/user/login')
@specialist_required
def delete_category(request, category_id):
    """
     Delete the category with id = category_id
     :param request: request
     :param category_id: int - category_id id
     :return: current page
     """
    try:
        del_category = QuestionCategory.objects.get(id=category_id)
        del_category.delete()
    except Exception as err:

        messages.error(request, f'Deleting category at "delete_category with id {category_id}" error occurred')
        logging.error(f'Deleting category at "delete_category with id {category_id}" error occurred\n{err}')
        return redirect('all_categories')
    return redirect('all_categories', permanent=True)


@login_required(login_url='/user/login')
@specialist_required
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

    per_page = 3
    paginator = Paginator(categories, per_page=per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    previous_page = request.POST.get('previous')
    if previous_page:
        redirect(previous_page)

    return render(request, 'institution/questions.html', {'questions': questions,
                                                          'categories': page_obj,
                                                          'categories_list': categories_list})


@login_required(login_url='/user/login')
@specialist_required
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


@login_required(login_url='/user/login')
@specialist_required
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
