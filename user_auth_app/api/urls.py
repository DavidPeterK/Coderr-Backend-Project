from django.urls import path
from .views import LoginView, RegistrationView, ProfileView, CustomerView, BusinessView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("customers/", CustomerView.as_view(), name="customers"),
    path("businesses/", BusinessView.as_view(), name="businesses"),
]
