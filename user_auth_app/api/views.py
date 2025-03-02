from user_auth_app.models import UserProfile
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from user_auth_app.api.serializers import RegistrationSerializer, ProfileSerializer, LoginSerializer
from user_auth_app.api.permissions import IsOwnerOrAdmin


class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.pk
            }, status=status.HTTP_201_CREATED)
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


class ProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def handle_exception(self, exc):
        if isinstance(exc, serializers.ValidationError):
            return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)


class BusinessProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.filter(type='business')
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]


class CustomerProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.filter(type='customer')
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
