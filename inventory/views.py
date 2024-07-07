from django.shortcuts import render
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import models
from . import serializers

# Create your views here.
class InventoryView(APIView):
    def get(self, request):
        product_list = models.Inventory.objects.all()
        serializer = serializers.InventorySerializer(product_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    
    def post(self, request):
        try:
            with transaction.atomic():
                models.Inventory.objects.create(**request.data)
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
            
            
class InventoryDeleteError(APIView):
    def post(self, request):
        try:
            models.Inventory.objects.filter(product_id=request.data.get('item_id')).delete()
            return Response(status=status.HTTP_200_OK)
        except models.Inventory.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            