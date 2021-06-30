from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True, min_length=5,
        error_messages={
            "blank": "Password cannot be empty.",
            "min_length": "Password too short.",
        },)

    class Meta:
        model = CustomUser
        fields = ('name', 'phone', 'email',
                  'created_at', 'bio', 'password')

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            phone=validated_data['phone'],
            name=validated_data['name'],
            bio=validated_data['bio'],
        )
        # user.bio = data.get('bio')
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_password(self, data):
        if data.isalnum():
            raise serializers.ValidationError(
                'password must have atleast one special character.')
        elif len(data) < 8:
            raise serializers.ValidationError(
                'password must have atleast 8 characters')
        elif data is None:
            raise serializers.ValidationError(
                'Password cannot be empty')
        return (data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        obj = CustomUser.objects.get(email=email)
        print(obj.email)
        user = authenticate(email=obj.email, password=password)
        print(user)
        if user:
            data['user'] = user
        else:
            msg = 'login failed'
            raise exceptions.ValidationError(msg)
        return data
