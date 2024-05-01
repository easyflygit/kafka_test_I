from rest_framework import serializers
from .models import Place, CategoryAnalytics


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['name', 'total_purchases', 'average_receipt']


class CategoryAnalyticsSerializer(serializers.ModelSerializer):
    place = serializers.CharField(source='place.name', read_only=True)
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = CategoryAnalytics
        fields = ['place', 'category', 'total_spent', 'average_receipt', 'total_purchases']
