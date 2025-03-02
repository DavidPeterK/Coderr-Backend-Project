from django.contrib.auth import authenticate
from user_auth_app.models import UserProfile
from rest_framework import serializers
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    repeated_password = serializers.CharField(write_only=True, required=True)
    type = serializers.ChoiceField(choices=UserProfile.TYPES, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "repeated_password", "type")

    def validate(self, data):
        errors = {}

        if not data.get('username'):
            errors['username'] = ["Benutzername ist erforderlich."]
        if not data.get('email'):
            errors['email'] = ["E-Mail ist erforderlich."]
        if not data.get('password'):
            errors['password'] = ["Passwort ist erforderlich."]
        if not data.get('repeated_password'):
            errors['repeated_password'] = [
                "Wiederholtes Passwort ist erforderlich."]

        if data.get('password') != data.get('repeated_password'):
            errors['password'] = [
                "Das Passwort ist nicht gleich mit dem wiederholten Passwort."]

        if User.objects.filter(username=data.get('username')).exists():
            errors['username'] = ["Dieser Benutzername ist bereits vergeben."]
        if User.objects.filter(email=data.get('email')).exists():
            errors['email'] = ["Diese E-Mail-Adresse wird bereits verwendet."]

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data):
        """ 
        Creates a new User instance along with a corresponding UserProfile.
        The `repeated_password` is removed from the data before saving.
        The user is created using `create_user()` to properly hash the password.
        """
        validated_data.pop("repeated_password", None)
        user_type = validated_data.pop("type")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        UserProfile.objects.create(user=user, type=user_type)

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError(
                        {"detail": ["Benutzerkonto ist deaktiviert."]})
                data['user'] = user
            else:
                raise serializers.ValidationError(
                    {"detail": ["Falsche Anmeldedaten."]})
        else:
            raise serializers.ValidationError(
                {"detail": ["Benutzername und Passwort sind erforderlich."]})

        return data


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", required=False)
    first_name = serializers.CharField(
        source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)

    class Meta:
        model = UserProfile
        fields = (
            "user", "username", "email", "first_name", "last_name", "file",
            "location", "tel", "description", "working_hours", "type",
            "created_at", "updated_at", "uploaded_at"
        )
        read_only_fields = ['user', 'created_at', 'updated_at', 'uploaded_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.type == 'customer':
            representation.pop('working_hours', None)
            representation.pop('tel', None)
            representation.pop('description', None)
            representation.pop('location', None)
        elif instance.type == 'business':
            representation.pop('uploaded_at', None)

        return representation

    def validate_email(self, value):
        if User.objects.filter(email=value).exclude(id=self.instance.user.id).exists():
            raise serializers.ValidationError(
                {"email": ["Diese E-Mail-Adresse wird bereits verwendet."]})
        return value

    def validate_tel(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError(
                {"tel": ["Die Telefonnummer darf nur Zahlen enthalten."]})
        return value

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        for field in ['first_name', 'last_name', 'email']:
            if field in user_data:
                setattr(user, field, user_data[field])

        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
