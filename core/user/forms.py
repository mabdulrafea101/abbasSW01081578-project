from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'user_type', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit user type choices to teacher and student for signup
        self.fields['user_type'].choices = [
            ('teacher', 'Teacher'),
            ('student', 'Student'),
        ]
        self.fields['user_type'].initial = 'teacher'

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['user_type'] == 'teacher':
            user.is_staff = True
        else:
            user.is_staff = False  # Ensure it's set explicitly for other types
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'user_type', 'phone')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_picture')
