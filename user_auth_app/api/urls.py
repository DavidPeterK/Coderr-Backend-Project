from django.urls import path
from user_auth_app.api.views import ProfileRetrieveUpdateView, BusinessProfileListView, CustomerProfileListView, LoginView, RegistrationView

urlpatterns = [
    path('profile/<int:pk>/', ProfileRetrieveUpdateView.as_view(),
         name='profile-retrieve-update'),
    path('profiles/business/', BusinessProfileListView.as_view(),
         name='business-profile-list'),
    path('profiles/customer/', CustomerProfileListView.as_view(),
         name='customer-profile-list'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
]
