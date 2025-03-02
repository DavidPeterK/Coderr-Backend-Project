from rest_framework import serializers
from order_app.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'business_user',
                  'offer_detail', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_status(self, value):
        if value not in ['in_progress', 'completed', 'cancelled']:
            raise serializers.ValidationError("Ungültiger Status.")
        return value
