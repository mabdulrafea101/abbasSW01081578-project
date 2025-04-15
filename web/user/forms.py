from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'user_type', 'student_id', 'phone')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control mb-1'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control mb-1'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control mb-1'}),
            'user_type': forms.Select(attrs={'class': 'form-control mb-1'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control mb-1'}),
            'phone': forms.TextInput(attrs={'class': 'form-control mb-1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit user type choices to teacher and student for signup
        self.fields['user_type'].choices = [
            ('teacher', 'Teacher'),
            ('student', 'Student'),
        ]
        self.fields['user_type'].initial = 'teacher'
        
        # Add form-control class to password fields
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-1'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-1'})

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
        fields = ('email', 'first_name', 'last_name', 'user_type', 'phone', 'student_id')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_picture')
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png,image/gif,image/webp,image/svg+xml,image/bmp,image/tiff'
            })
        }
        
    def clean_profile_picture(self):
        image = self.cleaned_data.get('profile_picture')
        if image:
            # Check file size
            if image.size > settings.MAX_UPLOAD_SIZE:
                raise ValidationError(f"File size must be no more than {settings.MAX_UPLOAD_SIZE/1024/1024}MB")
                
            # Django automatically validates the file extension based on the upload_to field
            # You can add additional validation here if needed
        return image


