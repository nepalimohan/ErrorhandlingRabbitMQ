import requests
from django.shortcuts import render
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import models
from . import serializers

# Create your views here.
class ProductView(APIView):
    def get(self, request):
        product_list = models.Product.objects.all()
        serializer = serializers.ProductSerializer(product_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def inventory_create_request(instance):
        data = {
            'id': instance.id
        }
        response = requests.post("http:127.0.0.1:8000/api/inventory/", json=data)
        if response.status_code == 200:
            return True
        return False
        
    
    def post(self, request):
        with transaction.atomic():
            quantity = request.data.pop('quantity')
            serializer = serializers.ProductSerializer(data = request.data)
            if serializer.is_valid():
                instance=serializer.save()
                
                inventory_creation = self.inventory_create_request(instance)
                
                if not inventory_creation:
                    raise Exception("Error creating inventory")
                
                response_data = {
                    'id': instance.id,
                    'message': "Product created successfully!"
                }
                return Response(response_data, status=status.HTTP_200_OK)