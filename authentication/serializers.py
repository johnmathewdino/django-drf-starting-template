from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name','is_staff')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.method == 'POST':
            email = attrs.get('email')
            username = attrs.get('username')
            password = attrs.get('password')

            if not email and not username:
                raise serializers.ValidationError("Email or username is required")

            # Unique email and username
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError("Email is already taken")
            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError("Username is already taken")

            # Password length
            if len(password) < 8:
                raise serializers.ValidationError("The password must be at least 8 characters long")


        return attrs

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=True)


    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')
        password = attrs.get('password')

        if not email and not username:
            raise serializers.ValidationError("Email or username is required")

        user = None
        if email:
            user = User.objects.filter(email=email).first()
        elif username:
            user = User.objects.filter(username=username).first()

        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        attrs['user'] = user
        return attrs

class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        user = User.objects.filter(email=email).first()
        if user is None:
            raise serializers.ValidationError("User with this email does not exist")
        return attrs

class ConfirmPasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, write_only=True)

    def __init__(self, *args, **kwargs):

        self.uid = kwargs.get('context').get('uid')
        self.token = kwargs.get('context').get('token')
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        new_password = attrs.get('new_password')

        # Decode the user ID from uidb64
        try:
            uid = urlsafe_base64_decode(self.uid).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid user ID")

        # Validate the token
        if not PasswordResetTokenGenerator().check_token(user, self.token):
            raise serializers.ValidationError("Invalid or expired token")

        # Ensure the new password meets the validation criteria
        if not new_password or len(new_password) < 8:
            raise serializers.ValidationError("The new password must be at least 8 characters long")

        # Save the new password
        user.set_password(new_password)
        user.save()

        return attrs

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')

        user = self.context['request'].user

        if not user.check_password(old_password):
            raise serializers.ValidationError("Invalid old password")

        # if len(new_password) < 8:
        #     raise serializers.ValidationError("The new password must be at least 8 characters long")

        return attrs
