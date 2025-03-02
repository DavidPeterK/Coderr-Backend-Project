from django.urls import path
from .views import ReviewListCreateView, ReviewRetrieveUpdateDestroyView, BaseInfoView

urlpatterns = [
    path('base-info/', BaseInfoView.as_view(), name='base-info'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewRetrieveUpdateDestroyView.as_view(),
         name='review-retrieve-update-destroy'),
]
