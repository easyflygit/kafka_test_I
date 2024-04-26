import os
import django
from kafka import KafkaConsumer
from django.conf import settings
import json

# Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'receipts_server.settings')

# Инициализируем Django
django.setup()

from producer.serializers import CheckSerializer
import logger


class KafkaMessageConsumer:
    def __init__(self):
        # Создаем объект KafkaConsumer для прослушивания сообщений из Kafka topic
        self.consumer = KafkaConsumer(
            'purchase_checks',  # указываем имя темы, из которой будем читать сообщения
            bootstrap_servers=[settings.KAFKA_SERVER],  # адрес и порт сервера Kafka
            group_id='my_consumer_group',  # уникальный идентификатор группы потребителей
            auto_offset_reset='earliest',  # смещение для чтения сообщений с самого начала темы
            enable_auto_commit=True,  # включаем автоматическое подтверждение смещений
            auto_commit_interval_ms=1000,  # интервал автоматического подтверждения смещений (в миллисекундах)
        )

    def consume_messages(self):
        # читаем сообщения из Kafka и обрабатываем их
        for message in self.consumer:
            # десериализуем полученное сообщение с помощью сериализатора
            data = json.loads(message.value.decode('utf-8'))
            check_instance = CheckSerializer(data=data)
            if check_instance.is_valid():
                # если данные валидны, сохраняем их в базу данных Django
                check_instance.save()
                logger.some_function('Purchase check saved: %s' % data)
                print('Purchase check have been saved')

            else:
                # если данные невалидны, выводим ошибки в консоль
                print('Invalid data:', check_instance.errors)
                logger.some_function('Invalid check data: %s')


# Создаем экземпляр KafkaMessageConsumer и запускаем прослушивание сообщений из Kafka
consumer = KafkaMessageConsumer()
consumer.consume_messages()
