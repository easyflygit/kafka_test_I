from kafka import KafkaConsumer
import json
import os
from django.conf import settings

import sys
sys.path.append('/Users/imac/Desktop/python_work/kafka_drf_test_task_I/receipts_server')

# Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'receipts_server.settings')
import django

django.setup()
from analytics.models import Check


class CheckConsumer:
    def __init__(self, topic, bootstrap_servers):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id='check-consumer-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

    def consume_checks(self):
        for message in self.consumer:
            # Получаем данные о чеке
            check_data = message.value

            # Обрабатываем чек
            self.process_check(check_data)

    def process_check(self, check_data):
        # Наша логика обработки чека здесь
        print("Received check:", check_data)

        # Проверяем наличие ключа 'items' в данных о чеке
        if 'items' in check_data:
            items = check_data['items']
            # Ваша логика обработки 'items'
            categories = set(item['category'] for item in items)
            print("Categories:", categories)
            total_amount = sum(item['price'] * item['quantity'] for item in items)
            print("Total amount:", total_amount)
        else:
            print("Error: 'items' key is missing in check data")
            return  # Выходим из метода, если отсутствует ключ 'items'
        check = Check(
            transaction_id=check_data['transaction_id'],
            timestamp=check_data['timestamp'],
            items=check_data['items'],
            total_amount=check_data['total_amount'],
            nds_amount=check_data['nds_amount'],
            tips_amount=check_data.get('tips_amount'),
            payment_method=check_data['payment_method']
        )
        # Пример: проверка способа оплаты и дополнительных данных
        if check_data['payment_method'] == 'credit_card':
            print("Paid by credit card")
        else:
            print("Paid by other method")


# Создаем экземпляр потребителя чеков
consumer = CheckConsumer(topic='purchase_checks',
                         bootstrap_servers=['localhost:9092'])

# Запускаем потребителя для приема чеков
consumer.consume_checks()