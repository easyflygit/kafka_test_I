import requests
import json


def send_purchase_check(check_data):
    url = 'http://127.0.0.1:8000/api/purchase_check/'
    try:
        response = requests.post(url, json=check_data)
        response.raise_for_status()  # Проверяем статус код ответа
        return response.json()  # Если успешно, возвращаем данные
    except Exception as e:
        print('Error', e)
        return {'error': str(e)}  # В случае ошибки возвращаем сообщение об ошибке
