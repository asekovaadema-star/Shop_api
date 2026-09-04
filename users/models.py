import random
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
def generate_code():
    return str(random.randint(100000, 999999))

class ConfirmationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirm_code')
    code = models.CharField(max_length=6, default=generate_code)