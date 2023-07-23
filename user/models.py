from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    description = models.TextField()
    pfp_url = models.CharField(max_length=254)
    dev_type = models.SmallIntegerField(max_length=4)
