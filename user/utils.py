import constant as con
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.shortcuts import render


def validate_field(**kwargs):
    for key, value in kwargs.items():
        if value is None:
            return key
        if len(value.strip()) < 1:
            return key
        if value.startswith(';', 2):
            return key


def mail_text_generator(request, user, template):
    current_site = get_current_site(request)
    subject = con.MAIL_ACTIVATION_TITLE
    message = render_to_string(template, {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    return user.email_user(subject, message)


def specialist_required(func):
    def wrapper(*args, **kwargs):
        if not args[0].user.groups.filter(name='specialist').exists():
            return render(args[0], 'institution/404.html', status=404)
        return func(*args, **kwargs)
    return wrapper


def donor_required(func):
    def wrapper(*args, **kwargs):
        if args[0].user.groups.filter(name='specialist').exists():
            return render(args[0], 'donor/404.html', status=404)
        return func(*args, **kwargs)
    return wrapper
