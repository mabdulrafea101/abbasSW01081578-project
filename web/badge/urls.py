# In badge/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('my-badges/', views.UserBadgesView.as_view(), name='user_badges'),
    path('all-badges/', views.AllBadgesView.as_view(), name='all_badges'),
    path('user/<int:pk>/badges/', views.UserProfileBadgesView.as_view(), name='user_profile_badges'),
]
