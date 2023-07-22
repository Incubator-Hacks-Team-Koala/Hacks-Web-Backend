from django.contrib.auth.models import User
from django.db import models


class Team(models.Model):
    team_name = models.CharField(primary_key=True, max_length=20)
    owner_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    team_name_pretty = models.CharField(max_length=20)
    description = models.TextField()
    passcode = models.CharField(max_length=50)


class TeamMembership(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    team_name = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        db_table = "team_membership"
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'team_name'], name='uniq_user_team'),
        ]
