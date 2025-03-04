from django.db import models
from django.contrib.auth.models import User


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='business_reviews')
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='customer_reviews')
    rating = models.IntegerField(
        choices=RATING_CHOICES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.business_user.username}"
