from django.db import models

# Create your models here.
# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    STATUS_CHOICES = (
        ('PENDING', 'PENDING'),
        ('APPROVED', 'APPROVED'),
        ('DENIED', 'DENIED'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    mobile = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

class UserOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
