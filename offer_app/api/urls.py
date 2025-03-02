from django.urls import path
from .views import OfferListCreateView, OfferRetrieveUpdateDestroyView, OfferDetailRetrieveView

urlpatterns = [
    path('offers/', OfferListCreateView.as_view(), name='offer-list-create'),
    path('offers/<int:pk>/', OfferRetrieveUpdateDestroyView.as_view(),
         name='offer-retrieve-update-destroy'),
    path('offerdetails/<int:pk>/', OfferDetailRetrieveView.as_view(),
         name='offer-detail-retrieve'),
]
