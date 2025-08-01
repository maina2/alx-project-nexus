# pollpro_backend/polls/views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Poll, Vote
from .serializers import PollSerializer, PollCreateSerializer, VoteSerializer, PollResultSerializer
from .permissions import IsAdmin, IsAuthenticated, IsAdminOrCreator

class CategoryChoicesView(generics.GenericAPIView):
    permission_classes = []  # Allow anyone to access

    @swagger_auto_schema(
        operation_description="List available poll categories",
        responses={200: openapi.Response('List of categories', openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'value': openapi.Schema(type=openapi.TYPE_STRING),
                    'label': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        ))}
    )
    def get(self, request):
        choices = [{'value': value, 'label': label} for value, label in Poll.CATEGORY_CHOICES]
        return Response(choices)

class PollCreateView(generics.CreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollCreateSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a new poll (authenticated users only)",
        responses={201: PollSerializer, 400: 'Invalid input', 401: 'Unauthorized'}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        poll = serializer.save()
        response_serializer = PollSerializer(poll, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class PollListView(generics.ListAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = []  # Allow anyone to list polls

    @swagger_auto_schema(
        operation_description="List all polls",
        responses={200: PollSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class PollDetailView(generics.RetrieveDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsAdminOrCreator]  # Admins or creators can delete

    def get_permissions(self):
        if self.request.method == 'GET':
            return []  # Allow anyone to retrieve
        return super().get_permissions()

    @swagger_auto_schema(
        operation_description="Retrieve a poll",
        responses={200: PollSerializer, 404: 'Not found'}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a poll (admin or creator only)",
        responses={204: 'No content', 403: 'Permission denied', 404: 'Not found'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class VoteView(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Cast a vote on a poll (authenticated users only)",
        responses={201: openapi.Response('Vote recorded', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'detail': openapi.Schema(type=openapi.TYPE_STRING)}
        )), 400: 'Invalid input', 401: 'Unauthorized', 404: 'Poll not found'}
    )
    def create(self, request, *args, **kwargs):
        try:
            poll = Poll.objects.get(pk=self.kwargs['pk'])
            serializer = self.get_serializer(data=request.data, context={'poll': poll, 'request': request})
            serializer.is_valid(raise_exception=True)
            Vote.objects.create(poll=poll, user=request.user, **serializer.validated_data)
            return Response({"detail": "Vote recorded"}, status=status.HTTP_201_CREATED)
        except Poll.DoesNotExist:
            return Response({"error": "Poll not found"}, status=status.HTTP_404_NOT_FOUND)

class VoteRetractView(generics.DestroyAPIView):
    queryset = Vote.objects.all()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retract a vote from a poll (authenticated users only)",
        responses={
            200: openapi.Response('Vote retracted', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'detail': openapi.Schema(type=openapi.TYPE_STRING)}
            )),
            400: 'No vote found or poll expired',
            401: 'Unauthorized',
            404: 'Poll not found'
        }
    )
    def destroy(self, request, *args, **kwargs):
        try:
            poll = Poll.objects.get(pk=self.kwargs['pk'])
            if not poll.is_active():
                return Response({"error": "Cannot retract vote on an expired poll"}, status=status.HTTP_400_BAD_REQUEST)
            vote = Vote.objects.get(poll=poll, user=request.user)
            vote.delete()
            return Response({"detail": "Vote retracted"}, status=status.HTTP_200_OK)
        except Poll.DoesNotExist:
            return Response({"error": "Poll not found"}, status=status.HTTP_404_NOT_FOUND)
        except Vote.DoesNotExist:
            return Response({"error": "No vote found to retract"}, status=status.HTTP_400_BAD_REQUEST)

class PollResultView(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollResultSerializer
    permission_classes = []  # Allow anyone to view results

    @swagger_auto_schema(
        operation_description="View poll results",
        responses={200: PollResultSerializer, 404: 'Not found'}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class UserPollHistoryView(generics.ListAPIView):
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List polls the user has voted in (authenticated users only)",
        responses={200: PollSerializer(many=True), 401: 'Unauthorized'}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return Poll.objects.filter(votes__user=user).distinct()