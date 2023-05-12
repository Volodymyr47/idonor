import logging
from copy import copy

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Question, Status, QuestionCategory
from django.core.paginator import Paginator


def main_page(request):
    return render(request, 'institution/main.html')


def get_all_donors(request):
    return render(request, 'institution/donors.html')


def all_categories(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        if category_name:
            try:
                add_category = QuestionCategory(name=category_name.upper(),
                                                inst_id=1)
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
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        if new_name is None:
            messages.error(request, f'Editing category at "edit_category with id {category_id}" error occurred')
            return redirect('all_categories')
        try:
            edited_category= QuestionCategory.objects.filter(id=category_id).get()
            edited_category.name = new_name
            edited_category.save()
        except Exception as err:
            logging.error(f'Editing category at "edit_category with id {category_id}" error occurred\n{err}')
            return redirect('all_categories')

    return redirect('all_categories', permanent=True)


def delete_category(request, category_id):
    try:
        edited_category = QuestionCategory.objects.get(id=category_id)
        edited_category.delete()
    except Exception as err:

        messages.error(f'Deleting category at "delete_category with id {category_id}" error occurred')
        logging.error(f'Deleting category at "delete_category with id {category_id}" error occurred\n{err}')
        return redirect('all_categories')
    return redirect('all_categories', permanent=True)


def all_questions(request):
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
        categories = QuestionCategory.objects.filter(id__in=categories_id).order_by('name')
        categories_list = QuestionCategory.objects.all().order_by('name')
    except Exception as err:
        messages.error(request, 'Questions or Categories selection error')
        logging.error(f'Questions or Categories selection error:\n{err}')

    per_page = 4
    paginator = Paginator(categories, per_page=per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'institution/questions.html', {'questions': questions,
                                                          'categories': page_obj,
                                                          'categories_list': categories_list})


def edit_question(request, question_id):
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
    try:
        edited_question = Question.objects.get(id=question_id)
        edited_question.delete()
    except Exception as err:
        print('err = ', err)
        messages.error(f'Deleting question at "delete_question with id {question_id}" error occurred')
        logging.error(f'Deleting question at "delete_question with id {question_id}" error occurred\n{err}')
        return redirect('all_questions')
    return redirect('all_questions', permanent=True)
