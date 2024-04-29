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
from analytics.models import Check, Place, CategoryAnalytics, CheckItem, Category
from producer import logger
from decimal import Decimal
from datetime import datetime
from django.utils import timezone


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

        if 'items' in check_data:
            items = check_data['items']
            categories = set(item['category'] for item in items)
            print("Categories:", categories)
            total_amount = Decimal(sum(Decimal(item['price']) * item['quantity'] for item in items))
            total_amount = Decimal(round(total_amount, 2))
            print("Total amount:", total_amount)
        else:
            print("Error: 'items' key is missing in check data")
            return

        # Проверяем что timestamp существует и в правильном формате
        if 'timestamp' not in check_data:
            print("Error: 'timestamp' key is missing in check data")
            return

        if 'total_amount' not in check_data:
            print("Error: 'total_amount' key is missing in check data")
            return

        if not categories:
            print("Error: At least one category must be provided in check data")
            return

        try:
            timestamp_str = check_data['timestamp']
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            print("Error: 'timestamp' is not in the correct format")
            return

        # Получаем данные о месте покупки и категориях товаров
        place_name = check_data.get('place_of_purchase', 'Store ABC')
        place, created = Place.objects.get_or_create(name=place_name)

        place.total_purchases += 1
        place.total_nds += Decimal(check_data['nds_amount'])
        if check_data.get('tips_amount'):
            place.total_tips += Decimal(check_data['tips_amount'])

        if total_amount > 0:
            place.average_receipt = (Decimal(place.average_receipt) * (place.total_purchases - 1) + total_amount) / place.total_purchases

        place.save()

        # Пример сохранения данных в модели CategoryAnalytics
        category_instances = []
        for category_name in categories:
            category_instance, created = Category.objects.get_or_create(name=category_name)
            category_instances.append(category_instance)

            if place.id:
                # Создаем или получаем объект CategoryAnalytics для каждой категории товаров
                try:
                    category_analytics = CategoryAnalytics.objects.get(category=category_instance, place=place)
                except CategoryAnalytics.DoesNotExist:
                    category_analytics = CategoryAnalytics.objects.create(category=category_instance, place=place)

                category_analytics.total_spent += total_amount
                category_analytics.total_purchases += 1

                if total_amount > 0:
                    category_analytics.average_receipt = \
                        (category_analytics.average_receipt *
                         (category_analytics.total_purchases - 1) + total_amount) / category_analytics.total_purchases
                category_analytics.save()
            else:
                print("Error: Couldn't get place_id for CategoryAnalytics")

        # Создаем или обновляем объект Check
        transaction_id = check_data['transaction_id']
        try:
            check = Check.objects.get(transaction_id=transaction_id)
        except Check.DoesNotExist:
            check = Check(transaction_id=transaction_id)

        check.timestamp = timezone.make_aware(timestamp)
        check.total_amount = check_data['total_amount']
        check.nds_amount = Decimal(check_data['nds_amount'])
        check.tips_amount = check_data.get('tips_amount')
        check.payment_method = check_data['payment_method']
        check.place_of_purchase = place  # сохраняем место покупки
        check.save()

        if category_instances:
            check.category.set(category_instances)
        else:
            print("Error: No category instances provided for the check")

        for item_data in check_data['items']:
            CheckItem.objects.create(
                check_ref=check,
                product_id=item_data['product_id'],
                quantity=item_data['quantity'],
                price=item_data['price']
            )
        logger.some_function('Purchase check saved: %s' % check_data)
        # Пример: проверка способа оплаты и дополнительных данных
        if check_data['payment_method'] == 'credit_card':
            print("Paid by credit card")
        else:
            print("Paid by other method")
        check.save()


# Создаем экземпляр потребителя чеков
consumer = CheckConsumer(topic='purchase_checks',
                         bootstrap_servers=['localhost:9092'])

# Запускаем потребителя для приема чеков
consumer.consume_checks()