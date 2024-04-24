from django.db import models


class Check(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True)
    timestamp = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    nds_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tips_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100)


class CheckItem(models.Model):
    check_ref = models.ForeignKey(Check, on_delete=models.CASCADE, related_name='items')
    product_id = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)


class Place(models.Model):
    place_id = models.CharField(max_length=100, unique=True)
    place_name = models.CharField(max_length=255)


class Purchase(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='purchases')
    total_purchases = models.PositiveIntegerField()
    average_receipt = models.DecimalField(max_digits=10, decimal_places=2)
    total_nds = models.DecimalField(max_digits=10, decimal_places=2)
    total_tips = models.DecimalField(max_digits=10, decimal_places=2)


class CategoryAnalytics(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='category_analytics')
    category = models.CharField(max_length=100)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2)
    average_receipt = models.DecimalField(max_digits=10, decimal_places=2)