from rest_framework.views import APIView
from . import serializers
from ... import models
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .import permissions


class ShopUserRegisterAPIView(APIView):
    serializer_class = serializers.ShopUserSerializer
    model = models.ShopUser

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(data=ser_data.data, status=status.HTTP_201_CREATED)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class EditProfileAPIView(APIView):
    serializer_class = serializers.EditProfileSerializer
    user_class = models.ShopUser
    permission_classes = [IsAuthenticated, permissions.IsProfileOwner]

    def get(self, request, user_id):
        user = get_object_or_404(self.user_class, id=user_id)
        self.check_object_permissions(request, user)
        ser_data = self.serializer_class(instance=user)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        user = get_object_or_404(self.user_class, id=user_id)
        self.check_object_permissions(request, user)
        ser_data = self.serializer_class(instance=user, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)