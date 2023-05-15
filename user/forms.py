from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from donor.models import Profile
from institution.models import Institution
import config

User = get_user_model()
institution = Institution.objects.get(full_name__icontains=config.INSTITUTION_CITY)


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='Ім\'я та по-Батькові')
    last_name = forms.CharField(label='Прізвище')
    email = forms.CharField(label='Електронна пошта')
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Пароль', required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Повторити Пароль', required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    phone = forms.CharField(label='Номер телефону', required=False)
    gender = forms.ChoiceField(label='Стать', choices=Profile.GENDER)
    birth_date = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'),
                                 label='Дата народження', required=True)
    home_addr = forms.CharField(label='Домашня адреса', required=False)
    work_addr = forms.CharField(label='Робоча адреса', required=False)
    inst_id = forms.IntegerField(label='',
                                 widget=forms.NumberInput(attrs={'hidden': 'True'}),
                                 initial=institution.pk, show_hidden_initial=False)

    class Meta:
        model = Profile
        fields = ('gender', 'birth_date', 'home_addr', 'work_addr', 'phone',)
        # widgets = {'inst_id': forms.NumberInput(attrs={'hidden': 'True'})}
