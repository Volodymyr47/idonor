from django.shortcuts import render


def home(request):
    return render(request, 'donor/home.html')


def pass_test(request):
    pass