from django.contrib.auth import authenticate, password_validation
from django.core.mail import EmailMultiAlternatives
from django.core.validators import RegexValidator
from django.template.loader import render_to_string
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from rj_project.users.models import Profile, User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
        )


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=64)

    def validate(self, data):
        user = authenticate(username=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid Credentials")
        if not user.is_verified:
            raise serializers.ValidationError("Account is not active yet")

        self.context["user"] = user
        return data

    def create(self, data):
        token, created = Token.objects.get_or_create(user=self.context["user"])
        return self.context["user"], token.key


class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    phone_regex = RegexValidator(
        regex=r"\+?1?\d{9,15}$",
        message="Phone number must be in the format: +9999999. Up 15 digits allowed.",
    )
    phone_number = serializers.CharField(max_length=17, validators=[phone_regex])
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, data):
        password = data["password"]
        password_confirmation = data["password_confirmation"]
        if password != password_confirmation:
            raise serializers.ValidationError("Password dont match")
        password_validation.validate_password(password)
        return data

    def create(self, data):
        data.pop("password_confirmation")
        user = User.objects.create_user(**data, is_verified=False)
        Profile.objects.create(user=user)
        token = self.send_confirmation_email(user)
        subject = f"Welcome @{user.username}! Verified you acoount"
        from_email = "from@example.com"
        text_content = render_to_string(
            "account/verification_sent.html", {"token": token, "user": user}
        )
        html_content = "Hola"
        msg = EmailMultiAlternatives(subject, text_content, from_email, [user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return user

    def send_confirmation_email(self, user):
        verification_token = "abc"
        return verification_token

    def gen_verification_token(self, user):
        return "abc"