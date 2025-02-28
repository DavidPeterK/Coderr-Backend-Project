from .permissions import IsOwnerOrAdmin
from user_auth_app.models import UserProfile
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from user_auth_app.models import UserProfile
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer
from .permissions import IsOwnerOrAdmin


class RegistrationView(APIView):
    """
    Handles user registration using APIView.

    - Uses RegistrationSerializer for validation.
    - If validation succeeds, creates a new user and UserProfile.
    - Generates and returns an authentication token.
    - Ensures that only custom serializer error messages are used.
    - Returns correct HTTP status codes and error formats.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)

            return Response(
                {
                    "token": token.key,
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Handles user login using APIView.

    - Uses LoginSerializer to validate input data.
    - If authentication succeeds, returns a token and user details.
    - If authentication fails, returns an error message in the correct API format.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)

            return Response(
                {
                    "token": token.key,
                    "username": user.username,
                    "email": user.email,
                    "user_id": user.id
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetailView(RetrieveUpdateAPIView):
    """
    Handles retrieving and updating user profiles.
    - Any authenticated user can retrieve profiles.
    - Only the owner can update their profile.
    """
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        """
        Get requests require the user to be authenticated.
        Patch requests require the user to be authenticated and to be the owner of the profile.
        """
        if self.request.method in ["PATCH", "PUT"]:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    def get_object(self):
        """
        Overrides the standard `get_object` to ensure users can only access their own profile.
        """
        if self.request.method in ["PATCH", "PUT"]:
            return get_object_or_404(UserProfile, user=self.request.user)
        return super().get_object()

    def patch(self, request, *args, **kwargs):
        """
        Updates the authenticated user's profile.
        Only the profile owner can perform this action.
        """
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerView(ListAPIView):
    """
    Returns a list of all customers.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(type="customer")


class BusinessView(ListAPIView):
    """
    Returns a list of all businesses.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(type="business")
