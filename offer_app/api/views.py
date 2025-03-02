from rest_framework import generics, permissions
from offer_app.models import Offer, OfferDetail
from offer_app.api.serializers import OfferSerializer, OfferDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend


class OfferListCreateView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'min_price', 'max_delivery_time']
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OfferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class OfferDetailRetrieveView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
