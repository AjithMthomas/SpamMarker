from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=128)

    def validate_password(self, value):
        if not any(char.isupper() for char in value):
            raise ValidationError("The password must contain at least one uppercase letter.")
        if not any(char.islower() for char in value):
            raise ValidationError("The password must contain at least one lowercase letter.")
        if not any(char.isdigit() for char in value):
            raise ValidationError("The password must contain at least one digit.")

    def clean(self):
        super().clean()
        self.validate_password(self.password)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.phone_number




class SpamNumber(models.Model):
    number = models.CharField(max_length=20, unique=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_spam')

    def __str__(self):
        return self.number




class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')
    search_query = models.CharField(max_length=255)
    search_type = models.CharField(max_length=20)  # 'name' or 'phone_number'
    search_results = models.JSONField()
    search_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
