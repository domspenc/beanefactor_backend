from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# --- USER MODEL ---
class DogUser(AbstractUser):
  available_treats = models.IntegerField(default=100)
  def __str__(self):
      return self.username