from django.contrib import admin
from .models import Check, CategoryAnalytics, Place, Category, CheckItem


admin.site.register(Check)
admin.site.register(CategoryAnalytics)
admin.site.register(Place)
admin.site.register(Category)
admin.site.register(CheckItem)
