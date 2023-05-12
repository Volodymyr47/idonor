from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string
from django.contrib.auth import logout, login, authenticate
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import Group

from .forms import RegistrationForm
from .tokens import account_activation_token


def pre_login(request):

    usr = authenticate(username=request.POST['username'],
                       password=request.POST['password'])

    if usr is not None:
        if not usr.is_active:
            return redirect(activation_sent_view)
        else:
            login(request, usr)
    else:
        messages.error(request, "Invalid username or password")
        return HttpResponseRedirect(reverse('user_login'))

    next_page = request.POST.get('next')
    if next_page:
        return redirect(next_page)
    return redirect('/')


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
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # user = form.save(commit=False)
            # user.username = form.cleaned_data.get('email')
            # user.save()
            user = form.save()
            user.refresh_from_db()
            user.profile.phone = form.cleaned_data.get('phone')
            group = Group.objects.get(name='customer')
            group.user_set.add(user)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            message = render_to_string('user/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('activation_sent')
    else:
        form = RegistrationForm()
    return render(request, 'user/registration.html', {'form': form})


def user_logout(request):
    """
    User logout function
    """
    logout(request)
    return render(request, 'user/logout.html')


def user_view(request):
    """
    Show user data
    """
    return render(request, 'user/user.html')
from django.shortcuts import render

# Create your views here.
