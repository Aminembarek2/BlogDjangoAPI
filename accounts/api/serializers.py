from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.serializers import CharField
from rest_framework.serializers import (
    ModelSerializer,
    )
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

    )
# from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
# from rest_framework_simplejwt.tokens import RefreshToken


# Registration serializer 
class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    re_password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ( "username",'email' ,'password', 're_password')
        extra_kwargs = {'username': {'required': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['re_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class UserLoginSerializer(serializers.Serializer):
    token = CharField(allow_blank=True, read_only=True)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        user = User.objects.filter(username=username)
        if user.exists() and user.count() == 1:
            user_obj=user.first()
        else:
            raise serializers.ValidationError("The username is not valid.")

        if user_obj:
            if not user_obj.check_password(data["password"]):
                raise serializers.ValidationError("Incorrect Login credentials")
        token = Token.objects.get_or_create(user=user_obj)[0].key
        data["message"] = "user logged in"
        data["username"] = user_obj.username
        data["token"] = token
        # t_obj=None
        # token=OutstandingToken.objects.filter(user=user_obj)
        # t_obj=token.first()
        # token = Token.objects.get(user=user_obj)
        # data['token'] = token
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

class UpdateUserSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        if validated_data.get('user'):
            user_data = validated_data.get('user')
            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid():
                user = user_serializer.update(instance=instance.user)
                validated_data['user'] = user
        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = ('username', 'email')
    

class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]