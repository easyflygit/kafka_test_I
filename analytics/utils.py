# from django.db.models import Sum, Avg
# from .models import Place, CategoryAnalytics, Check
#
#
# def calculate_analytics():
#     # Рассчитываем общую сумму налогов и чаевых за промежуток времени
#     total_taxes = Check.objects.aggregate(total_nds=Sum('nds_amount'), total_tips=Sum('tips_amount'))
#
#     # Рассчитываем общую аналитику для каждого места покупки
#     places = Place.objects.all()
#     for place in places:
#         # Рассчитываем количество покупок в данном месте
#
#         total_purchases = Check.objects.filter(place_of_purchase=place).count()
#
#         # Расситываем средний чек в данном месте
#         average_receipt = Check.objects.filter(
#             place_of_purchase=place).aggregate(average_receipt=Avg('total_amount'))
#
#         # Рассчитываем аналитику по категориям товаров для данного места
#         categories = CategoryAnalytics.objects.all()
#         for category in categories:
#             total_spent = Check.objects.filter(
#                 place_of_purchase=place, category=category).aggregate(total_spent=Sum('total_amount'))
#             average_receipt_category = Check.objects.filter(
#                 place_of_purchase=place, category=category).aggregate(average_receipt=Avg('total_amount'))
#
#             # Создаем или обновляем запись аналитики по категории товаров
#             category_analytics, created = CategoryAnalytics.objects.get_or_create(place=place, category=category)
#             category_analytics.total_spent = total_spent['total_spent'] or 0
#             category_analytics.average_receipt = average_receipt_category['average_receipt'] or 0
#             category_analytics.save()
#
#         # Создаем или обновляем запись аналитики для данного места
#         place.total_purchases = total_purchases
#         place.average_receipt = average_receipt['average_receipt'] or 0
#         place.total_nds = total_taxes['total_nds'] or 0
#         place.total_tips = total_taxes['total_tips'] or 0
#         place.save()