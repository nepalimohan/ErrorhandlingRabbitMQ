import pika
import json
import requests
from inventory.models import Inventory

def compensate_inventory(ch, method, properties, body):
    data = json.loads(body)
    item_id = data['item_id']
    # quantity = data['quantity']

    # Compensate inventory
    try:
        # data.pop('quantity')
        # response = requests.post("http://127.0.0.1:8000/api/inventory/delete/", json=data)
        # if response != 200:
        #     raise Exception('delete vayena')
        inventory_item = Inventory.objects.get(id=item_id)
        print(inventory_item.product_id)
        inventory_item.delete()
    except Exception as e:
        print(e)

def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='compensate_inventory')

    channel.basic_consume(queue='compensate_inventory',
                          on_message_callback=compensate_inventory,
                          auto_ack=True)

    channel.start_consuming()
