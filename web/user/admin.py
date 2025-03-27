from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationFormAdmin(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'user_type', 'phone','username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit user type choices to teacher and student for signup
        self.fields['user_type'].choices = [
            ('manager', 'Manager'),
            ('student', 'Student'),
            ('teacher', 'Teacher'),
        ]
        self.fields['user_type'].required = False


class UserAdmin(UserAdmin):
    list_display = ('email',
                    'username',
                    'user_type',
                    'is_staff',
                    'updated_at',
                    'is_account_confirmed',)
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': (
            'user_type',
            'phone',
            'is_account_confirmed',
        )}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': (
            'first_name',
            'last_name',
            'email',
            'user_type',
            'phone',
            'is_account_confirmed',
        )}),
    )
    add_form = CustomUserCreationFormAdmin


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Profile)
