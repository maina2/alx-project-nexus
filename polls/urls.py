# pollpro_backend/polls/urls.py
from django.urls import path
from .views import PollCreateView, PollListView, PollDetailView, VoteView, PollResultView, CategoryChoicesView

urlpatterns = [
    path('', PollListView.as_view(), name='poll_list'),
    path('create/', PollCreateView.as_view(), name='poll_create'),
    path('<int:pk>/', PollDetailView.as_view(), name='poll_detail'),
    path('<int:pk>/vote/', VoteView.as_view(), name='poll_vote'),
    path('<int:pk>/results/', PollResultView.as_view(), name='poll_results'),
    path('categories/', CategoryChoicesView.as_view(), name='category_choices'),
]