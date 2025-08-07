# pollpro_backend/polls/urls.py
from django.urls import path
from .views import (
    PollCreateView, 
    PollListView, 
    PollDetailView, 
    VoteView, 
    PollResultView, 
    CategoryChoicesView, 
    VoteRetractView,
    UserPollHistoryView
)

urlpatterns = [
    path('', PollListView.as_view(), name='poll_list'),
    path('create/', PollCreateView.as_view(), name='poll_create'),
    path('categories/', CategoryChoicesView.as_view(), name='category_choices'),
    path('user-history/', UserPollHistoryView.as_view(), name='user_poll_history'),
    path('<int:pk>/', PollDetailView.as_view(), name='poll_detail'),
    path('<int:pk>/vote/', VoteView.as_view(), name='poll_vote'),
    path('<int:pk>/retract/', VoteRetractView.as_view(), name='vote_retract'),
    path('<int:pk>/results/', PollResultView.as_view(), name='poll_results'),
]