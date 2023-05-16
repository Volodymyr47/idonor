import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string
from django.contrib.auth import logout, login, authenticate
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import Group

import config
import constant as con
from .utils import validate_field
from .tokens import account_activation_token
from institution.models import Institution
from donor.models import Profile, History, Test

User = get_user_model()


def make_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        not_valid_field = validate_field(email=email,
                                         password1=password)
        if not_valid_field:
            messages.error(request, con.REG_FIELD_POPULATION_ERROR.format(field=not_valid_field))
            return redirect('make_login')

        usr = authenticate(email=email, password=password)

        if usr is not None:
            if not usr.is_active:
                return redirect(activation_sent_view)
            else:
                login(request, usr)
        else:
            messages.error(request, "Invalid username or password")

        next_page = request.POST.get('next')
        if next_page:
            return redirect(next_page)

        return redirect('/')
    return render(request, 'user/login.html', )


def activation_sent_view(request):
    return render(request, 'user/activation_sent.html')


def activate(request, uidb64, token):
    """
    User account activation
    """
    message = ''
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, TimeoutError) as err:
        user = None
        message = err

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, 'user/activation_invalid.html', {'message': message})


def register(request):
    """
    User registrations function
    """
    institution = Institution.objects.get(full_name__icontains=config.INSTITUTION_CITY)

    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        birthday = request.POST.get('birthday')
        home_addr = request.POST.get('home_addr')
        work_addr = request.POST.get('work_addr')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        not_valid_field = validate_field(email=email,
                                         first_name=first_name,
                                         last_name=last_name,
                                         phone=phone,
                                         birthday=birthday,
                                         home_addr=home_addr,
                                         password1=password1)

        if not_valid_field:
            messages.error(request, con.REG_FIELD_POPULATION_ERROR.format(field=not_valid_field))
            return redirect('register')

        if password1 != password2:
            messages.error(request, con.PASSWORDS_ERROR)
            return redirect('register')

        new_user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=first_name + ' ' + last_name,
            is_active=False,
            password=password2
        )
        group = Group.objects.get(name='donor')
        group.user_set.add(new_user)
        profile = Profile.objects.create(
            phone=phone,
            gender=gender,
            birth_date=birthday,
            home_addr=home_addr,
            work_addr=work_addr,
            inst_id=institution.id,
            user_id=new_user.id,
            signup_confirmation=False
        )

        current_site = get_current_site(request)
        subject = con.MAIL_ACTIVATION_TITLE
        message = render_to_string('user/activation_request.html', {
            'user': new_user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
            'token': account_activation_token.make_token(new_user),
        })
        new_user.email_user(subject, message)
        return redirect('activation_sent')

    profile = Profile()
    return render(request, 'user/registration.html', {'genders': (profile.GENDER[0][1],
                                                                  profile.GENDER[1][1])})


def user_logout(request):
    """
    User logout function
    """
    logout(request)
    return render(request, 'user/logout.html')


def get_user_info(request, user_id):
    """
    Show user data
    """
    user_info = None
    try:
        user_info = User.objects.filter(id=user_id).all()
    except Exception as err:
        logging.error(f'Function "Get_user_info" error: \n{err}')

    return render(request, 'user/info.html', {'user_info': user_info})


def password_sent(request):
    return render(request, 'user/password-sent.html')


def change_password(request, uidb64, token):

    if request.method == 'POST':
        password1 = request.POST.get('new_password1')
        password2 = request.POST.get('new_password2')

        if password1 != password2 or password2.startswith(';', 2):
            messages.error(request, con.NEW_PASSWORD_ERROR)
            return redirect('change_password', uidb64, token)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.filter(id=uid).first()
            user.set_password(password2)
            user.save()
            return redirect('home')

        except (TypeError, ValueError, OverflowError, TimeoutError) as err:
            logging.error(f'Password changing error:\n{err}')
            messages.error(request, 'Password changing error')
            return redirect('make_login')
    return render(request, 'user/password-change.html', {'uidb64':uidb64,
                                                    'token': token})


def recover_password(request):
    user = None
    if request.method == 'POST':
        email = request.POST.get('email_for_recover')
        try:
            user = User.objects.filter(email=email).first()
            if user is None:
                messages.warning(request, f'No user found with email {email}')
                return redirect('make_login')

        except Exception as err:
            messages.error(request, 'Password recovering error')
            logging.error(f'Password recovering error:\n{err}')
            return redirect('make_login')

    current_site = get_current_site(request)
    subject = con.PASSWORD_RESET_MAIL
    message = render_to_string('user/password-change-request.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    user.email_user(subject, message)
    return redirect('password_sent')
