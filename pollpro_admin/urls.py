# pollpro_backend/pollpro_admin/urls.py
from django.urls import path
from .views import (
    UserListCreateView,
    UserDetailView,
    PollListCreateView,
    PollDetailView,
    VoteListView,
    VoteDetailView,
)

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='admin_user_list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='admin_user_detail'),
    path('polls/', PollListCreateView.as_view(), name='admin_poll_list'),
    path('polls/<int:pk>/', PollDetailView.as_view(), name='admin_poll_detail'),
    path('votes/', VoteListView.as_view(), name='admin_vote_list'),
    path('votes/<int:pk>/', VoteDetailView.as_view(), name='admin_vote_detail'),
]