from django.contrib.auth import authenticate
from user_auth_app.models import UserProfile
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    repeated_password = serializers.CharField(write_only=True, required=True)
    type = serializers.ChoiceField(choices=UserProfile.TYPES, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "repeated_password", "type")

    def validate_email(self, value):
        """ 
        Checks if the provided email already exists in the database.
        If the email is already registered, a validation error is raised.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                ["Diese E-Mail-Adresse wird bereits verwendet."])
        return value

    def validate_username(self, value):
        """ 
        Checks if the provided username is already taken.
        If the username exists, a validation error is returned.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                ["Dieser Benutzername ist bereits vergeben."])
        return value

    def validate(self, data):
        """ 
        Ensures that the provided password and repeated password match.
        If they do not match, a validation error is raised.
        """
        if data["password"] != data["repeated_password"]:
            raise serializers.ValidationError(
                {"password": ["Das Passwort und das wiederholte Passwort stimmen nicht überein."]})
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
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        """ 
        Validates user credentials according to the API specifications.
        """
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError(
                {"username": ["Benutzername oder Passwort ist falsch."]})

        data["user"] = user
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
            "created_at", "updated_at"
        )
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate_email(self, value):
        """
        Validiert, ob die E-Mail-Adresse bereits verwendet wird.
        """
        if User.objects.filter(email=value).exclude(id=self.instance.user.id).exists():
            raise serializers.ValidationError(
                "Diese E-Mail-Adresse wird bereits verwendet."
            )
        return value

    def validate_tel(self, value):
        """
        Validiert, ob die Telefonnummer ein gültiges Format hat.
        """
        if value and not value.isdigit():
            raise serializers.ValidationError(
                "Die Telefonnummer darf nur Zahlen enthalten."
            )
        return value

    def update(self, instance, validated_data):
        """
        Aktualisiert das UserProfile und die zugehörigen User-Daten.
        """
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
