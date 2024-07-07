from django.core.management.base import BaseCommand
from core.consumers import start_consuming

class Command(BaseCommand):
    help = 'Start RabbitMQ consumers'

    def handle(self, *args, **kwargs):
        start_consuming()
