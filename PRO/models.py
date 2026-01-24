from django.db import models

from django.db import models

class UserProfile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    id_num = models.CharField(max_length=10, unique=True)
    username = models.CharField(max_length=10, unique=True)
    phone_num = models.CharField(max_length=11, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone_num})"
    
class Course(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title