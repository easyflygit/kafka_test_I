from django.db import models


class Place(models.Model):
    name = models.CharField(max_length=255)
    total_purchases = models.PositiveIntegerField(default=0)
    average_receipt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_nds = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_tips = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Place'
        verbose_name_plural = 'Places'


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class CategoryAnalytics(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='category_analytics')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_analytics')
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    average_receipt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_purchases = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.category} Analytics for {self.place}"

    class Meta:
        verbose_name = 'Category Analytics'
        verbose_name_plural = 'Category Analytics'


class Check(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True)
    timestamp = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    nds_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tips_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=100)
    place_of_purchase = models.ForeignKey(Place, on_delete=models.CASCADE, null=True, blank=True)  # поле для места покупки
    category = models.ManyToManyField(Category, null=True, blank=True, related_name='checks')  # поле для категории товаров

    def __str__(self):
        return self.transaction_id

    class Meta:
        verbose_name = 'Check'
        verbose_name_plural = 'Checks'


class CheckItem(models.Model):
    check_ref = models.ForeignKey(Check, on_delete=models.CASCADE, related_name='items')
    product_id = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Check {self.check_ref}, Product {self.product_id}"

