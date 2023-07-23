from django.contrib.auth.models import User
from django.db import models


class Team(models.Model):
    team_name = models.CharField(unique=True, max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    team_name_pretty = models.CharField(max_length=20)
    description = models.TextField()
    passcode = models.CharField(max_length=50)

    def __str__(self):
        return self.team_name


class TeamMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        db_table = "team_membership"
        constraints = [
            models.UniqueConstraint(fields=['user', 'team'], name='uniq_user_team'),
        ]
