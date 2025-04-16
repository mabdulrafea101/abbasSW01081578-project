from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy

from django.db.models import F, Window, Count
from django.db.models.functions import Rank
#from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.views import LoginView

from .mixins import ManagerRequiredMixin
from .models import CustomUser, Profile, PointHistory
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
    success_url = reverse_lazy('pending_users')

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
        # Return a proper queryset instead of a dictionary
        return CustomUser.objects.filter(is_account_confirmed=False)



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
        # Always return the logged-in user's profile
        return self.request.user.profile
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data if needed
        context['user'] = self.request.user
        # You could add stats, badges, events, etc.
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'user/profile_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        # Always update the logged-in user's profile
        return self.request.user.profile
        
    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated successfully.")
        return super().form_valid(form)


# In user/views.py
class UserLevelDashboardView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'user/level_dashboard.html'
    context_object_name = 'profile_user'
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        profile = user.profile
        
        # Calculate progress to next level
        level_thresholds = profile.get_level_thresholds()
        current_level = profile.current_level
        
        if current_level < len(level_thresholds) + 1:
            if current_level == 1:
                min_points = 0
            else:
                min_points = level_thresholds[current_level - 2]
                
            max_points = level_thresholds[current_level - 1]
            points_needed = max_points - profile.total_points
            progress_percentage = ((profile.total_points - min_points) / 
                                   (max_points - min_points)) * 100
        else:
            # Max level reached
            points_needed = 0
            progress_percentage = 100
            
        context.update({
            'total_points': profile.total_points,
            'current_level': profile.current_level,
            'points_needed': points_needed,
            'progress_percentage': progress_percentage,
            'recent_points': user.point_history.all()[:10],
            'participating_events_count': user.participating_events.count(),
            'organizing_events_count': user.organizing_events.count(),
            'ratings_given_count': user.given_ratings.count(),
        })
        
        return context
    

# In user/views.py


class UserLevelHistoryView(LoginRequiredMixin, ListView):
    """View to display the user's point history"""
    model = PointHistory
    template_name = 'user/level_history.html'
    context_object_name = 'point_history'
    paginate_by = 10
    
    def test_func(self):
        # Only students can view the leaderboard
        return self.request.user.user_type == 'student'
    def get_queryset(self):
    # Get the current user's point history ordered by most recent first
    # Only works for student users
        if self.request.user.user_type == 'student':
            return PointHistory.objects.filter(
                user=self.request.user
            ).order_by('-timestamp')
        else:
            # Return empty queryset for non-students
            return PointHistory.objects.none()

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = user.profile
        
        # Add level and points information to context
        context.update({
            'total_points': profile.total_points,
            'current_level': profile.current_level,
            'username': user.username,
        })
        
        return context


class LevelLeaderboardView(LoginRequiredMixin, ListView):
    """View to display all users ranked by level and points"""
    model = Profile
    template_name = 'user/level_leaderboard.html'
    context_object_name = 'leaderboard'
    paginate_by = 20
    
    def test_func(self):
        # Only students can view the leaderboard
        return self.request.user.user_type == 'student'
    
    def get_queryset(self):
    # Get all student users with their profiles, ordered by level and points
        profiles = Profile.objects.select_related('user').filter(
            user__is_account_confirmed=True,
            user__user_type='student'  # Add this filter for students only
        ).order_by('-current_level', '-total_points')

        
        # Add rank to each profile
        rank = 1
        user_id = self.request.user.id
        leaderboard_with_rank = []
        current_user_rank = None
        
        for profile in profiles:
            entry = {
                'rank': rank,
                'username': profile.user.username,
                'user_type': profile.user.get_user_type_display(),
                'level': profile.current_level,
                'points': profile.total_points,
                'is_current_user': profile.user.id == user_id
            }
            
            if profile.user.id == user_id:
                current_user_rank = rank
                
            leaderboard_with_rank.append(entry)
            rank += 1
            
        return leaderboard_with_rank
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = user.profile
        
        # Find the current user's rank
        for entry in context['leaderboard']:
            if entry['is_current_user']:
                context['user_rank'] = entry['rank']
                break
                
        # Add user's level information
        context.update({
            'total_points': profile.total_points,
            'current_level': profile.current_level,
        })
        
        return context
