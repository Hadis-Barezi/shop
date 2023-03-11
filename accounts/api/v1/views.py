from rest_framework.views import APIView
from . import serializers
from ... import models
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, get_list_or_404
from .import permissions
from rest_framework import viewsets


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

    def setup(self, request, *args, **kwargs):
        self.user = get_object_or_404(self.user_class, pk=kwargs["user_id"])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # user = get_object_or_404(self.user_class, id=user_id)
        self.check_object_permissions(request, self.user)
        ser_data = self.serializer_class(instance=self.user)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        # user = get_object_or_404(self.user_class, id=user_id)
        self.check_object_permissions(request, self.user)
        ser_data = self.serializer_class(instance=self.user, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
    serializer_class = serializers.ChangePasswordSerializer
    shop_user_class = models.ShopUser
    permission_classes = [IsAuthenticated, permissions.IsProfileOwner]

    def put(self, request, user_id):
        user = get_object_or_404(self.shop_user_class, id=user_id)
        self.check_object_permissions(request, user)
        ser_data = self.serializer_class(instance=user, data=request.data)
        if ser_data.is_valid():
            cd = ser_data.validated_data
            user.change_password(new_password=cd['new_password'], old_password=cd['password'])
            user.save()
            data = {'message': 'your password changed successfully.'}
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressViewSet(viewsets.ViewSet):
    serializer_class = serializers.AddressSerializer
    permission_classes = [IsAuthenticated,]
    user_model = models.ShopUser
    address_model = models.Address

    def list(self, request):
        shop_user = get_object_or_404(self.user_model, id=request.user.id)
        addresses = get_list_or_404(self.address_model, shop_user=shop_user)
        ser_data = self.serializer_class(instance=addresses, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def create(self, request):
        shop_user = get_object_or_404(self.user_model, id=request.user.id)
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            new_address = self.address_model.objects.create(**ser_data.data, shop_user=shop_user)
            # new_address.shop_user = shop_user
            # new_address.save()
            return Response(data=ser_data.data, status=status.HTTP_201_CREATED)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        shop_user = get_object_or_404(self.user_model, id=request.user.id)
        address = get_object_or_404(self.address_model, id=pk)
        if shop_user == address.shop_user:
            ser_data = self.serializer_class(data=request.data, instance=address)
            if ser_data.is_valid():
                ser_data.save()
                return Response(data=ser_data.data, status=status.HTTP_200_OK)
            return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
        data = {'message': 'you are not allowed!'}
        return Response(data=data, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        shop_user = get_object_or_404(self.user_model, id=request.user.id)
        address = get_object_or_404(self.address_model, id=pk)
        if shop_user == address.shop_user:
            address.delete()
            data = {'message': 'Address deleted.'}
            return Response(data=data, status=status.HTTP_204_NO_CONTENT)
        data = {'message': 'you are not allowed!'}
        return Response(data=data, status=status.HTTP_403_FORBIDDEN)