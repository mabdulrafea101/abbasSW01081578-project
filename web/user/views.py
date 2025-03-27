from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
#from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.views import LoginView

from .mixins import ManagerRequiredMixin
from .models import CustomUser, Profile
from .forms import CustomUserCreationForm, ProfileForm

# Create your views here.


class CustomLoginView(LoginView):
    template_name = 'user/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_account_confirmed and not user.is_superuser:
            messages.error(
                self.request,
                'Your account is pending approval from the admin.'
            )
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        if user.user_type == 'student':
            return reverse('student_dashboard')
        elif user.user_type == 'teacher':
            return reverse('teacher_dashboard')
        elif user.user_type == 'manager':
            return reverse('manager_dashboard')
        else:
            return reverse('home')  # Or a default dashboard
    

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'user/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Your account has been created and is pending approval from the admin.'
        )
        print(form.cleaned_data)

        return response


class AllUsersListView(ManagerRequiredMixin, ListView):
    model = CustomUser
    template_name = 'user/all_users.html'
    context_object_name = 'all_users'

    def get_queryset(self):
        return CustomUser.objects.exclude(is_superuser=True)


class PendingUserListView(ManagerRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'user/pending_users.html'
    context_object_name = 'pending_users'

    def test_func(self):
        return self.request.user.user_type == 'manager'

    def get_queryset(self):
        return CustomUser.objects.filter(is_account_confirmed=False)\
            .exclude(is_superuser=True)
    

class ConfirmUserView(ManagerRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    fields = ['is_account_confirmed']
    template_name = 'user/confirm_user.html'
    success_url = reverse_lazy('pending-users')

    def test_func(self):
        # Restrict access to manager only
        return self.request.user.user_type == 'manager'

    def form_valid(self, form):
        # Automatically set is_account_confirmed to True
        form.instance.is_account_confirmed = True
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Account for {self.object.username} has been confirmed."
        )
        return response

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'manager':
            return {}
        elif user.user_type == 'teacher':
            return {}
        else:  # student
            return {}


class BaseDashboardView(LoginRequiredMixin, ListView):
    # Common dashboard logic here (e.g., template_name)
    context_object_name = 'dashboard_data'
    model = CustomUser  # Or remove this if the queryset is always custom


class ManagerDashboardView(BaseDashboardView):
    template_name = 'user/manager_dashboard.html'

    def get_queryset(self):
        return CustomUser.objects.all()  # All users for manager


class TeacherDashboardView(BaseDashboardView):
    template_name = 'user/teacher_dashboard.html'
    
    def get_queryset(self):
        return CustomUser.objects.filter(user_type='student')  # Teachers see students


class StudentDashboardView(BaseDashboardView):
    template_name = 'user/student_dashboard.html'

    def get_queryset(self):
        return CustomUser.objects.filter(user_type='teacher')  # Students see teachers


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'user/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'user/profile_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user.profile