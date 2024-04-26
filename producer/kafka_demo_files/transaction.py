import json

from kafka import KafkaProducer
from kafka import KafkaConsumer

ORDER_KAFKA_TOPIC = 'send_purchase_check'
ORDER_CONFIRMED_KAFKA_TOPIC = 'order_confirmed'

consumer = KafkaConsumer(
    ORDER_KAFKA_TOPIC,
    bootstrap_servers='localhost:9092'
)
producer = KafkaProducer(
    bootstrap_servers='localhost:9092'
)

print("Gonna start listening...")
while True:
    for message in consumer:
        print("Ongoing transaction...")
        consumed_message = json.loads(message.value.decode())
        print(consumed_message)

        transaction_id = consumed_message['transaction_id']
        timestamp = consumed_message['timestamp']

        total_amount = consumed_message['total_amount']
        nds_amount = consumed_message['nds_amount']

        data = {
            "transaction_id": transaction_id,
            "timestamp": timestamp,
            "total_amount": total_amount,
            "nds_amount": nds_amount,
        }

        print("Successful transaction...")
        producer.send(
            ORDER_CONFIRMED_KAFKA_TOPIC,
            json.dumps(data).encode('utf-8')
        )