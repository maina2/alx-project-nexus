# pollpro_backend/users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegisterSerializer, UserSerializer
from polls.permissions import IsAdmin
from .models import CustomUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user.",
        request_body=UserRegisterSerializer,
        responses={
            201: openapi.Response("User registered successfully", UserSerializer),
            400: "Invalid input"
        }
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve details of the authenticated user.",
        responses={
            200: openapi.Response("User details retrieved successfully", UserSerializer),
            401: "Unauthorized"
        }
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update details of the authenticated user.",
        request_body=UserSerializer,
        responses={
            200: openapi.Response("User details updated successfully", UserSerializer),
            400: "Invalid input",
            401: "Unauthorized"
        }
    )
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Logout by blacklisting the refresh token.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh'],
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description="The refresh token to blacklist.")
            }
        ),
        responses={
            205: "Successfully logged out.",
            400: "Refresh token is missing or invalid."
        }
    )
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AdminUserManagementView(APIView):
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        operation_description="List all users (admin only).",
        responses={
            200: openapi.Response("List of all users", UserSerializer(many=True)),
            403: "Permission denied"
        }
    )
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)