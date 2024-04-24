import requests
import json

# Данные вашего чека покупки
check_data = {
    "items": [
        {"product_id": "product_id_1", "quantity": 2, "price": 10.99, "category": "groceries"},
        {"product_id": "product_id_2", "quantity": 1, "price": 5.49, "category": "electronics"}
    ],
    "total_amount": 27.47,
    "nds_amount": 2.47,
    "tips_amount": 3.0,
    "payment_method": "credit_card"
}

# URL вашего API эндпоинта
url = 'http://127.0.0.1:8000/api/purchase_check/'

# Отправляем POST-запрос
response = requests.post(url, json=check_data)

# Печатаем результат
print(response.json())


