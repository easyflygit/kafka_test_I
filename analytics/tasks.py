import os
import sys
from celery import shared_task
from django.db.models import Sum, Avg

sys.path.append('/Users/imac/Desktop/python_work/kafka_drf_test_task_I/receipts_server')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'receipts_server.settings')

import django
django.setup()

from analytics.models import Place, CategoryAnalytics, Check, Category


@shared_task
def calculate_analytics():
    # Рассчитываем общую сумму налогов и чаевых за промежуток времени
    total_taxes = Check.objects.aggregate(total_nds=Sum('nds_amount'), total_tips=Sum('tips_amount'))

    # Рассчитываем общую аналитику для каждого места покупки
    places = Place.objects.all()
    for place in places:
        # Рассчитываем количество покупок в данном месте

        total_purchases = Check.objects.filter(place_of_purchase=place).count()

        # Расситываем средний чек в данном месте
        average_receipt = Check.objects.filter(
            place_of_purchase=place).aggregate(average_receipt=Avg('total_amount'))

        # Рассчитываем аналитику по категориям товаров для данного места
        for check in Check.objects.filter(place_of_purchase=place):
            categories = check.category.all()
            for category_instance in categories:
                total_spent = Check.objects.filter(
                    place_of_purchase=place, category=category_instance).aggregate(total_spent=Sum('total_amount'))
                average_receipt_category = Check.objects.filter(
                    place_of_purchase=place, category=category_instance).aggregate(average_receipt=Avg('total_amount'))

                # Создаем или обновляем запись аналитики по категории товаров
                category_analytics, created = CategoryAnalytics.objects.get_or_create(place=place, category=category_instance)
                category_analytics.total_spent = total_spent['total_spent'] or 0
                category_analytics.average_receipt = average_receipt_category['average_receipt'] or 0
                category_analytics.save()
            else:
                print("No categories found for the check.")

        for category_instance in Category.objects.all():
            # Аннотируем каждый чек агрегированным значением total_amount для данной категории
            checks_with_category = Check.objects.filter(place_of_purchase=place, category=category_instance)
            total_spent_for_category = checks_with_category.aggregate(total_spent=Sum('total_amount'))
            # checks_with_category = checks_with_category.annotate(total_spent=Sum('total_amount'))
            # checks_with_category = checks_with_category.annotate(average_receipt=Avg('total_amount'))

            # Получаем сумму total_spent и среднее average_receipt для данной категории
            # total_spent = checks_with_category.aggregate(total_spent=Sum('total_spent'))
            # average_receipt_category = checks_with_category.aggregate(average_receipt=Avg('average_receipt'))

            # Создаем или обновляем запись аналитики по категории товаров
            category_analytics, created = CategoryAnalytics.objects.get_or_create(place=place, category=category_instance)
            category_analytics.total_spent = total_spent_for_category['total_spent'] or 0
            # category_analytics.average_receipt = average_receipt_category['average_receipt'] or 0
            category_analytics.save()

        # Создаем или обновляем запись аналитики для данного места
        place.total_purchases = total_purchases
        place.average_receipt = average_receipt['average_receipt'] or 0
        place.total_nds = total_taxes['total_nds'] or 0
        place.total_tips = total_taxes['total_tips'] or 0
        place.save()