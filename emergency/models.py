from django.contrib.auth.models import User
from django.db import models



# Create your models here.
class UserRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=100)
    issue = models.TextField()

    def __str__(self):
        return f"{self.email}"




