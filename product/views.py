import requests
from django.shortcuts import render
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import models
from . import serializers

import pika
import json

# Create your views here.
class ProductView(APIView):
    INVENTORY_URL = "http://127.0.0.1:8000/api/inventory/"
    def get(self, request):
        product_list = models.Product.objects.all()
        serializer = serializers.ProductSerializer(product_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def inventory_create_request(self, instance, quantity):
        data = {
            'product_id': instance.id,
            'total_quantity': quantity,
        }
        response = requests.post(self.INVENTORY_URL, json=data)
        if response.status_code == 200:
            return True
        return False
        
    
    def post(self, request):
        try:
            with transaction.atomic():
                quantity = request.data.pop('quantity')
                serializer = serializers.ProductSerializer(data = request.data)
                if serializer.is_valid():
                    instance=serializer.save()
                    
                    inventory_creation = self.inventory_create_request(instance, quantity)
                    
                    if not inventory_creation:
                        raise Exception("Error creating inventory")
                    
                    response_data = {
                        'id': instance.id,
                        'message': "Product created successfully!"
                    }
                    raise Exception('test')
                    return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            # Compensate Inventory if an error occurs
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
            channel = connection.channel()
            channel.queue_declare(queue='compensate_inventory')

            event = {
                "item_id": instance.id,
                "quantity": quantity
            }

            channel.basic_publish(exchange='',
                                routing_key='compensate_inventory',
                                body=json.dumps(event))

            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)