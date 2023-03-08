from rest_framework.views import APIView
from . import serializers
from ... import models
from rest_framework.response import Response
from rest_framework import status


class ShopUserRegisterAPIView(APIView):
    serializer_class = serializers.ShopUserSerializer
    model = models.ShopUser

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(data=ser_data.data, status=status.HTTP_201_CREATED)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
