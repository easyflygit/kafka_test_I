from kafka import KafkaProducer
import json
import uuid
import time
import logging

# Создаем экземпляр Kafka Producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])


# Функция для отправки чека покупки в тему Kafka
def send_purchase_check(check):
    # Генерируем уникальный идентификатор транзакции
    transaction_id = str(uuid.uuid4())
    # Добавляем временную метку совершения покупки
    check['timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%S")
    # Добавляем уникальный идентификатор транзакции
    check['transaction_id'] = transaction_id
    # Преобразуем чек в JSON
    json_check = json.dumps(check)
    # Отправляем чек в тему Kafka
    producer.send('purchase_checks', json_check.encode('utf-8'))
    # Дожидаемся подтверждения от сервера Kafka
    producer.flush()
    print(f"Sent purchase check to Kafka topic 'purchase_checks': {json_check}")


 # Пример использования
if __name__ == "__main__":
    # Пример чека покупки
    example_check = {
        "items": [
            {"product_id": "product_id_1", "quantity": 2, "price": 10.99, "category": "groceries"},
            {"product_id": "product_id_2", "quantity": 1, "price": 5.49, "category": "electronics"},
        ],
        "total_amount": 27.47,
        "nds_amount": 2.47,
        "tips_amount": 3.0,
        "payment_method": "credit_card"
    }
    # Отправляем тестовый чек покупки
    send_purchase_check(example_check)

