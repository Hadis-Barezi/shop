from ... import models
from rest_framework import serializers


class ShopUserSerializer(serializers.ModelSerializer):
    user_model = models.ShopUser
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.ShopUser
        fields = ['id', 'f_name', 'l_name', 'phone', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Password must be equal!")
        return data

    def create(self, validated_data):
        del(validated_data['confirm_password'])
        return self.user_model.objects.create_user(**validated_data)


class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShopUser
        fields = ['id', 'f_name', 'l_name', 'phone', 'email']


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_new_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.ShopUser
        fields = ['password', 'new_password', 'confirm_new_password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("Password must be equal!")
        return data


