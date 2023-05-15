from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)


@admin.register(User)
class UserAdmin(UserAdmin):

    list_display = ('username', 'email', 'is_superuser', 'is_active')
    list_filter = ('is_active', 'groups')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'first_name',
                           'last_name', 'date_joined', 'is_active')}),

        ('Permissions', {'fields': ('is_superuser', 'groups', 'user_permissions')}),
    )

    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    search_fields = ('username', 'email')
    ordering = ('username', 'email')

    filter_horizontal = ()
