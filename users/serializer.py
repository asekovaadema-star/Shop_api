from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from .models import ConfirmationCode

class UserConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)

    def validate_code(self, code):
        try:
            confirmation = ConfirmationCode.objects.get(code=code)
        except ConfirmationCode.DoesNotExist:
            raise ValidationError('Code not found!')

        user = confirmation.user
        user.is_active = True
        user.save()
        confirmation.delete()

        return code

class UserBaseSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 150)
    password = serializers.CharField()

class UserAuthSerializer(UserBaseSerializer):
    pass

class UserCreateSerializer(UserBaseSerializer):

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('User already exists !')