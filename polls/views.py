from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Poll, Vote
from .serializers import PollSerializer, PollCreateSerializer, VoteSerializer, PollResultSerializer
from .permissions import IsAdmin, IsAuthenticated

class CategoryChoicesView(generics.GenericAPIView):
    permission_classes = []  # Allow anyone to access

    def get(self, request):
        choices = [{'value': value, 'label': label} for value, label in Poll.CATEGORY_CHOICES]
        return Response(choices)

class PollCreateView(generics.CreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollCreateSerializer
    permission_classes = [IsAuthenticated]

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

class PollDetailView(generics.RetrieveDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsAdmin]  # Only admins can delete

    def get_permissions(self):
        if self.request.method == 'GET':
            return []  # Allow anyone to retrieve
        return super().get_permissions()

class VoteView(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            poll = Poll.objects.get(pk=self.kwargs['pk'])
            serializer = self.get_serializer(data=request.data, context={'poll': poll, 'request': request})
            serializer.is_valid(raise_exception=True)
            Vote.objects.create(poll=poll, user=request.user, **serializer.validated_data)
            return Response({"detail": "Vote recorded"}, status=status.HTTP_201_CREATED)
        except Poll.DoesNotExist:
            return Response({"error": "Poll not found"}, status=status.HTTP_404_NOT_FOUND)

class PollResultView(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollResultSerializer
    permission_classes = []  # Allow anyone to view results