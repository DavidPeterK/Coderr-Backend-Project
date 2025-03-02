from rest_framework import serializers
from offer_app.models import Offer, OfferDetail


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image',
                  'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'offer', 'title', 'revisions',
                  'delivery_time_in_days', 'price', 'features', 'offer_type']
        read_only_fields = ['id']
