from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile


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


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Profile)