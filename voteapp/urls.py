from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='principal'),
    path('register/', views.register, name='register'),
    path('profile/edit/', views.profileEdit, name='profile-edit'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('profile/<int:id>/edit/', views.profile_edit, name='edit-profile'),
    path('profile/<int:id>/followers/add/', views.addFollower, name='add-follower'),
    path('logout/', views.signout, name='logout'),
    path('home/', views.voteHome, name='home'),
    path('home/all-votes/', views.allVotes, name='all-votes'),
    path('home/<int:id>/', views.addVote, name='add-vote'),
    path('home/<int:id>/second-vote/', views.AddVoteTwo, name='add-vote-two'),
    path('newvote/', views.newVote, name='new-vote'),
    path('home/votedetail/<int:id>/', views.VoteDetail, name='vote-detail') ,
    path('home/search/', views.searchUser, name='search'),
    path('home/delete/<int:id>/', views.delete_post, name='delete-post'),
    path('home/searchresponsive/', views.searchResponsive, name='search-responsive'),
    path('notification/<int:notification_id>/vote/<int:vote_id>/', views.voteNotification, name='vote-notification'),
    path('notification/<int:notification_id>/profile/<int:profile_id>/', views.followNotification, name='follow-notification')
]