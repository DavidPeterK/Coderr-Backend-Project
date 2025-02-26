from rest_framework.generics import ListAPIView
from user_auth_app.models import UserProfile
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer


class RegistrationView(APIView):
    """
    Handles user registration using APIView.

    - Uses RegistrationSerializer for validation.
    - If validation succeeds, creates a new user and UserProfile.
    - Generates and returns an authentication token.
    - Ensures that only custom serializer error messages are used.
    - Returns correct HTTP status codes and error formats.
    """

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

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)

            return Response(
                {
                    "token": token.key,
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    """
    Handles retrieving and updating user profiles.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns the user's profile details.
        """
        profile = request.user.userprofile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        """
        Updates the user's profile.
        """
        profile = request.user.userprofile
        serializer = ProfileSerializer(
            profile, data=request.data, partial=True)

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
