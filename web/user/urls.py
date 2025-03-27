from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    #path('dashboard/', views.DashboardView.as_view(), name='dashboard'), # No longer needed
    path('pending-users/', views.PendingUserListView.as_view(),
         name='pending-users'),
    path('confirm-user/<int:pk>/', views.ConfirmUserView.as_view(),
         name='confirm-user'),
    path('profile/', views.ProfileDetailView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile-update'),

    # Dashboard URLs for different user types
    path('student/dashboard/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('teacher/dashboard/', views.TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('manager/dashboard/', views.ManagerDashboardView.as_view(), name='manager_dashboard'),
]
