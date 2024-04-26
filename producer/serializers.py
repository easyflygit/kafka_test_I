from rest_framework import serializers
from producer.models import Check, CheckItem


class CheckItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckItem
        fields = ('product_id', 'quantity', 'price', 'category')


class CheckSerializer(serializers.ModelSerializer):
    items = CheckItemSerializer(many=True)

    class Meta:
        model = Check
        fields = ('transaction_id', 'timestamp', 'items', 'total_amount', 'nds_amount', 'tips_amount', 'payment_method')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        check = Check.objects.create(**validated_data)
        for item_data in items_data:
            CheckItem.objects.create(check_ref=check, **item_data)
        return check

    def validate(self, data):
        """
        Валидация данных чека перед сохранением
        """
        total_amount = data.get('total_amount')
        nds_amount = data.get('nds_amount')
        tips_amount = data.get('tips_amount')

        # Проверка, что общая сумма чека больше суммы НДС и чаевых
        if total_amount <= nds_amount + tips_amount:
            raise serializers.ValidationError("Общая сумма чека должна быть больше суммы НДС и чаевых.")

        return data