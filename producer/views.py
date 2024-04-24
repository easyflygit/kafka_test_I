from rest_framework.views import APIView
from rest_framework.response import Response
from kafka import KafkaProducer
import json
import uuid
import time
from .models import Check, CheckItem
from .serializers import CheckSerializer
from .utils import send_purchase_check


class CheckView(APIView):
    def post(self, request):
        serializer = CheckSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PurchaseCheckAPIView(APIView):
    def post(self, request):
        # Получаем данные о чеке покупки из запроса
        check_data = request.data

        # Добавляем уникальный идентификатор транзакции, если он есть
        if 'transaction_id' in request.data:
            check_data['transaction_id'] = request.data['transaction_id']
        else:
            check_data['transaction_id'] = str(uuid.uuid4())

        # Создаем экземпляр Kafka Producer
        producer = KafkaProducer(bootstrap_servers='localhost:9092')

        # Добавляем временную метку совершения покупки
        check_data['timestamp'] = time.strftime('%Y-%m-%dT%H:%M:%S')

        # Преобразуем чек в формат JSON
        json_check = json.dumps(check_data)

        # Отправляем чек в тему Kafka
        producer.send('purchase_checks', json_check.encode('utf-8'))

        # Ждем подтверждения от сервера Kafka
        producer.flush()

        # Возвращаем ответ с подтверждением отправки чека
        return Response({'message': 'Purchase check sent to Kafka topic "purchase_checks".'})

# class PurchaseCheckAPIView(APIView):
#     def post(self, request):
#         # Получаем данные о чеке покупки из запроса
#         check_data = request.data
#
#         # Отправляем чек покупки
#         response_data = send_purchase_check(check_data)
#
#         # Возвращаем ответ
#         return Response(response_data)






