from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    TYPES = (
        ('customer', 'Customer'),
        ('business', 'Business'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPES, blank=False)
    file = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    location = models.CharField(max_length=100, default='')
    tel = models.CharField(max_length=15, default='', blank=True, null=True)
    description = models.TextField(default='', blank=True, null=True)
    working_hours = models.CharField(
        max_length=50, default='', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.type})"
