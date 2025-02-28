from django.urls import path
from .views import LoginView, RegistrationView, ProfileDetailView, CustomerView, BusinessView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),
    path("profiles/customer/", CustomerView.as_view(), name="customers"),
    path("profiles/business/", BusinessView.as_view(), name="businesses"),
]
