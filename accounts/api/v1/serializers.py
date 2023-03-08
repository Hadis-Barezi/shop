from ... import models
from rest_framework import serializers


class ShopUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = models.ShopUser
        fields = ['f_name', 'l_name', 'phone', 'email', 'password', 'confirm_password']

    def validate(self, data):
        if data ['password'] != data['confirm_password']:
            raise serializers.ValidationError("Password must be equal!")
        return data
