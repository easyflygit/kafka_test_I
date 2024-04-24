from kafka import KafkaConsumer

# Создаем объект KafkaConsumer
consumer = KafkaConsumer(
    'purchase_checks',  # указываем имя темы, из которой будем читать сообщения
    bootstrap_servers='localhost:9092',  # указываем адрес и порт сервера Kafka
    group_id='my_consumer_group',  # уникальный идентификатор группы потребителей
    auto_offset_reset='earliest',  # устанавливаем смещение для чтения сообщений с самого начала темы
    enable_auto_commit=True,  # включаем автоматическое подтверждение смещений
    auto_commit_interval_ms=1000,  # устанавливаем интервал автоматического подтверждения смещений в миллисекундах
)

# читаем сообщения их темы и выводим их в консоль
for message in consumer:
    print(f"Received message: {message.value.decode('utf-8')}")

# закрываем соединение с сервером Kafka
consumer.close()