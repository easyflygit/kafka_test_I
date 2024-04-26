import json
import time

from kafka import KafkaProducer

ORDER_KAFKA_TOPIC = 'send_purchase_check'
ORDER_LIMIT = 15

producer = KafkaProducer(bootstrap_servers='localhost:9092')

print("Going to be generating order after 3 seconds")
print("Will generate one unique order every 3 seconds")

for i in range(1, ORDER_LIMIT+1):
    data = {
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

    producer.send(
        ORDER_KAFKA_TOPIC,
        json.dumps(data).encode('utf-8')
    )
    print(f"Done sending...{i}")
