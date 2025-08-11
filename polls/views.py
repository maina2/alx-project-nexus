# pollpro_backend/polls/views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import NotFound
from .models import Poll, Vote
from .serializers import PollSerializer, PollCreateSerializer, VoteSerializer, PollResultSerializer,PollUpdateSerializer
from .permissions import IsAdmin, IsAuthenticated, IsAdminOrCreator, IsPollCreator

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
    
class UserPollListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PollSerializer

    def get_queryset(self):
        # Filter polls by the authenticated user
        return Poll.objects.filter(creator=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        """
        List all polls created by the authenticated user.
        """
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "No polls found for this user"}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """
        Set the creator to the authenticated user during poll creation.
        """
        serializer.save(creator=self.request.user)

class UserPollRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsPollCreator]
    serializer_class = PollSerializer
    queryset = Poll.objects.all()

    def get_object(self):
        # Retrieve a specific poll and check creator permission
        pk = self.kwargs.get('pk')
        try:
            poll = Poll.objects.get(pk=pk)
            self.check_object_permissions(self.request, poll)
            return poll
        except Poll.DoesNotExist:
            raise NotFound(detail="Poll not found")

    def update(self, request, *args, **kwargs):
        """
        Update a specific poll created by the user.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = PollUpdateSerializer(instance, data=request.data, partial=partial, context={'request': request})
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """
        Delete a specific poll created by the user.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class PollListView(generics.ListAPIView):
    serializer_class = PollSerializer
    permission_classes = []  # Allow anyone to list polls

    @swagger_auto_schema(
        operation_description="List all polls with optional category filter",
        manual_parameters=[
            openapi.Parameter(
                name='category',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=[choice[0] for choice in Poll.CATEGORY_CHOICES],
                description='Filter polls by category (e.g., TECH, ENT, SPRT, POL, LIFE, EDU). Leave empty for all categories.'
            )
        ],
        responses={200: PollSerializer(many=True)}
    )
    def get_queryset(self):
        """
        This view returns a list of all polls with optional category filtering.
        """
        queryset = Poll.objects.all().order_by('-created_at')  # Order by newest first
        category = self.request.query_params.get('category', None)
        
        if category:
            # Validate that the category is one of the allowed choices
            valid_categories = [choice[0] for choice in Poll.CATEGORY_CHOICES]
            if category in valid_categories:
                queryset = queryset.filter(category=category)
            else:
                # If invalid category provided, return empty queryset
                return Poll.objects.none()
        
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Override list method to add additional context or debugging
        """
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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
            
            # Check if poll is active
            if not poll.is_active():
                return Response(
                    {"error": "Cannot vote on an expired poll"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if user has already voted
            existing_vote = Vote.objects.filter(poll=poll, user=request.user).first()
            if existing_vote:
                return Response(
                    {"error": "You have already voted on this poll"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
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
    permission_classes = []  

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
        return Poll.objects.filter(votes__user=user).distinct().order_by('-created_at')