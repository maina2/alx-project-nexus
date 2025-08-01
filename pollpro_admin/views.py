# pollpro_backend/pollpro_admin/views.py
from rest_framework import generics
from django.contrib.auth.models import User
from polls.models import Poll, Vote
from .serializers import UserSerializer, AdminPollSerializer, VoteSerializer
from polls.permissions import IsAdmin
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        operation_description="List all users or create a new user (admin only)",
        responses={200: UserSerializer(many=True), 201: UserSerializer, 403: 'Permission denied'}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new user (admin only)",
        responses={201: UserSerializer, 400: 'Invalid input', 403: 'Permission denied'}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        operation_description="Retrieve a user (admin only)",
        responses={200: UserSerializer, 403: 'Permission denied', 404: 'Not found'}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a user (admin only)",
        responses={200: UserSerializer, 400: 'Invalid input', 403: 'Permission denied', 404: 'Not found'}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a user (admin only)",
        responses={204: 'No content', 403: 'Permission denied', 404: 'Not found'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class PollListCreateView(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = AdminPollSerializer
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        operation_description="List all polls or create a new poll (admin only)",
        responses={200: AdminPollSerializer(many=True), 201: AdminPollSerializer, 403: 'Permission denied'}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new poll (admin only)",
        responses={201: AdminPollSerializer, 400: 'Invalid input', 403: 'Permission denied'}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class PollDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = AdminPollSerializer
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        operation_description="Retrieve a poll (admin only)",
        responses={200: AdminPollSerializer, 403: 'Permission denied', 404: 'Not found'}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a poll (admin only)",
        responses={200: AdminPollSerializer, 400: 'Invalid input', 403: 'Permission denied', 404: 'Not found'}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a poll (admin only)",
        responses={204: 'No content', 403: 'Permission denied', 404: 'Not found'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class VoteListView(generics.ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        operation_description="List all votes (admin only)",
        responses={200: VoteSerializer(many=True), 403: 'Permission denied'}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class VoteDetailView(generics.DestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        operation_description="Delete a vote (admin only)",
        responses={204: 'No content', 403: 'Permission denied', 404: 'Not found'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)