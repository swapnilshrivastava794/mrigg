from django.db import models
import random


def generate_otp():
    return str(random.randint(100000, 999999))


class EmailOTP(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.otp}"
