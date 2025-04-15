
from django.urls import path
from . import views

urlpatterns = [
    # View event ratings page
    path('event/<int:pk>/ratings/', views.EventRatingView.as_view(), name='event_rating'),
    
    # Rate an organizer
    path('event/<int:event_pk>/rate-organizer/<int:organizer_pk>/', 
         views.RateOrganizerView.as_view(), name='rate_organizer'),
    
    # Add a comment to a rating
    path('rating/<int:rating_pk>/comment/', 
         views.AddCommentView.as_view(), name='add_comment'),
    
    # Add a reply to a comment
    path('comment/<int:comment_pk>/reply/', 
         views.AddReplyView.as_view(), name='add_reply'),
    
    # Delete a comment
    path('comment/<int:pk>/delete/', 
         views.DeleteCommentView.as_view(), name='delete_comment'),
    
    # Delete a reply
    path('reply/<int:pk>/delete/', 
         views.DeleteReplyView.as_view(), name='delete_reply'),
    
    # View all ratings given by the current user
    path('my-ratings/', 
         views.UserRatingsListView.as_view(), name='user_ratings'),
]
