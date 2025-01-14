from django.contrib.auth.models import User
from rest_framework import serializers
from . import models


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


from cloudinary.uploader import upload

class UserInfoSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = models.UserInfo
        fields = ['bio', 'website', 'location', 'profile_picture']

    def update(self, instance, validated_data):
        if 'profile_picture' in validated_data:
            # Upload the image to Cloudinary
            image = validated_data.pop('profile_picture')
            upload_result = upload(image)
            instance.profile_picture = upload_result['url']
        return super().update(instance, validated_data)
