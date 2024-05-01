from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from kafka import KafkaProducer
import json
import uuid
import time
from analytics.models import Check
from producer.serializers import CheckSerializer


class CheckView(APIView):
    def post(self, request):
        serializer = CheckSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, requests):
        checks = Check.objects.all()
        serializer = CheckSerializer(checks, many=True)
        return Response(serializer.data)


class PurchaseCheckAPIView(APIView):
    def post(self, request):
        # Получаем данные о чеке покупки из запроса
        check_data = request.data

        # Добавляем уникальный идентификатор транзакции, если он есть
        if 'transaction_id' not in request.data:
            check_data['transaction_id'] = str(uuid.uuid4())
        # Добавляем временную метку совершения покупки
        check_data['timestamp'] = time.strftime('%Y-%m-%dT%H:%M:%S')
        check_data['items'] = [
            {"product_id": "product_id_1", "quantity": 2, "price": 10.99, "category": "groceries"},
            {"product_id": "product_id_2", "quantity": 1, "price": 5.49, "category": "electronics"}
        ]
        check_data['total_amount'] = 27.47
        check_data['nds_amount'] = 2.47
        check_data['tips_amount'] = 3.0
        check_data['payment_method'] = 'credit_card'

        # Создаем экземпляр Kafka Producer
        producer = KafkaProducer(bootstrap_servers='localhost:9092')

        # Преобразуем чек в формат JSON
        json_check = json.dumps(check_data)

        # Отправляем чек в тему Kafka
        producer.send('purchase_checks', json_check.encode('utf-8'))

        # Ждем подтверждения от сервера Kafka
        producer.flush()

        # Возвращаем ответ с подтверждением отправки чека
        return Response(json_check, status=status.HTTP_201_CREATED)







