# pollpro_backend/pollpro_admin/views.py
from rest_framework import generics
from django.contrib.auth.models import User
from polls.models import Poll, Vote
from .serializers import UserSerializer, AdminPollSerializer, VoteSerializer
from polls.permissions import IsAdmin

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

class PollListCreateView(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = AdminPollSerializer
    permission_classes = [IsAdmin]

class PollDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = AdminPollSerializer
    permission_classes = [IsAdmin]

class VoteListView(generics.ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAdmin]

class VoteDetailView(generics.DestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAdmin]