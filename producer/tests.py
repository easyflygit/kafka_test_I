import unittest

from django.test import TestCase
from django.utils.timezone import make_aware
from datetime import datetime
from rest_framework.test import APIClient, APITestCase
from unittest.mock import MagicMock, patch
from .models import Check
from .serializers import CheckSerializer
from rest_framework import status
from django.urls import reverse
from .kafka_producer import send_purchase_check


# class CheckViewTest(TestCase):
#     def test_create_check(self):
#         # Создаем экземпляр клиента для работы с API
#         client = APIClient()
#
#         # Предположим, у вас есть данные, которые вы ожидаете отправить
#         # в POST запросе. Представим их в виде JSON строки.
#         check_data = {
#             "transaction_id": "unique_transaction_id",
#             "timestamp": "2024-02-07T12:34:56",
#             "items": [
#                 {
#                     "product_id": "product_id_1",
#                     "quantity": 2,
#                     "price": 10.99,
#                     "category": "groceries"
#                 },
#                 {
#                     "product_id": "product_id_2",
#                     "quantity": 1,
#                     "price": 5.49,
#                     "category": "electronics"
#                 }
#             ],
#             "total_amount": 27.47,
#             "nds_amount": 2.47,
#             "tips_amount": 3.0,
#             "payment_method": "credit_card"
#         }
#
#         # Вызываем метод create_check() с переданными данными
#         response = client.post('/api/checks/', check_data, format='json')
#
#         # Проверяем, что полученный ответ соответствует ожиданиям
#         self.assertEqual(response.status_code, 201)  # Предполагаем, что мы ожидаем статус "Created"
#         self.assertEqual(Check.objects.count(), 1)  # Проверяем, что создан только один объект Check
#         # Дополнительно можно проверить значения полей созданного объекта
#         # check = Check.objects.get(transaction_id="unique_transaction_id")
#         # self.assertEqual(check.total_amount, 27.47)
#         # и так далее
#
#
# class KafkaProducerMock:
#     def __init__(self):
#         self.send = MagicMock
#
from django.test import TestCase
from django.utils.timezone import make_aware
from unittest.mock import patch
from datetime import datetime
from rest_framework.test import APIClient
from .models import Check
from . import send_check


class CheckViewTest(TestCase):
    @patch('producer.kafka_producer.send_purchase_check')
    def test_create_check(self, mock_send_purchase_check):
        client = APIClient()
        check_data = {
            "transaction_id": "unique_transaction_id",
            "timestamp": "2024-02-07T12:34:56",
            "items": [
                {"product_id": "product_id_1", "quantity": 2, "price": 10.99, "category": "groceries"},
                {"product_id": "product_id_2", "quantity": 1, "price": 5.49, "category": "electronics"}
            ],
            "total_amount": 27.47,
            "nds_amount": 2.47,
            "tips_amount": 3.0,
            "payment_method": "credit_card"
        }
        response = client.post('/api/checks/', check_data, format='json')
        self.assertEqual(response.status_code, 201)

        # Проверяем, что метод send_purchase_check был вызван один раз
        # mock_send_purchase_check.assert_called_once_with(check_data)




