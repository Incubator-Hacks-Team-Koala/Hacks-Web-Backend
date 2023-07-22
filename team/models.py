from django.db import models


class Team(models.Model):
    team_name = models.CharField(primary_key=True, max_length=20)
    description = models.CharField(max_length=200)
    passcode = models.CharField(max_length=20)

