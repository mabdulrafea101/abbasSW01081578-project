from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('all-users/', views.AllUsersListView.as_view(), name='all_users'),
    path('pending-users/', views.PendingUserListView.as_view(),
         name='pending_users'),
    path('confirm-user/<int:pk>/', views.ConfirmUserView.as_view(),
         name='confirm_user'),
    path('profile/', views.ProfileDetailView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_update'),

    # Dashboard URLs for different user types
    path('student/dashboard/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('teacher/dashboard/', views.TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('manager/dashboard/', views.ManagerDashboardView.as_view(), name='manager_dashboard'),
    path('level/', views.UserLevelDashboardView.as_view(), name='user_level'),
    path('level/history/', views.UserLevelHistoryView.as_view(), name='level_history'),
    path('level/leaderboard/', views.LevelLeaderboardView.as_view(), name='level_leaderboard'),
    path('top-organizers/', views.TopOrganizersView.as_view(), name='top_organizers'),
    path('top-participants/', views.TopParticipantsView.as_view(), name='top_participants'),
]
