from django.db import models


class Place(models.Model):
    place_id = models.AutoField(primary_key=True)
    place_name = models.CharField(max_length=255)
    total_purchases = models.PositiveIntegerField(default=0)
    average_receipt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_nds = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_tips = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.place_name


class CategoryAnalytics(models.Model):
    category_name = models.CharField(max_length=255)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    average_receipt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_purchases = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.category_name


class Check(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True)
    timestamp = models.DateTimeField()
    items = models.JSONField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    nds_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tips_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=100)
    place_of_purchase = models.CharField(max_length=100, null=True, blank=True)  # поле для места покупки
    category = models.CharField(max_length=100, null=True, blank=True)  # поле для категории товаров

    def __str__(self):
        return self.transaction_id


