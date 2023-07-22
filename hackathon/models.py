from django.contrib.auth.models import User
from django.db import models

from team.models import Team


class Hackathon(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        db_table = "hackathon_hackathon"

class HackathonTeamEnrol(models.Model):
    hack_id = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    team_name = models.ForeignKey(Team, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=20)
    project_description = models.TextField()
    project_presentation_url = models.CharField(max_length=254)
    project_code_url = models.CharField(max_length=254)

    class Meta:
        db_table = "hackathon_team_enrol"


class HackathonAward(models.Model):
    hack_id = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.TextField()
    open_date = models.DateTimeField()
    close_date = models.DateTimeField()
    winner_team_name = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        db_table = "hackathon_award"


class HackathonAwardVote(models.Model):
    award_id = models.ForeignKey(HackathonAward, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    team_name = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        db_table = "hackathon_award_vote"
        constraints = [
            models.UniqueConstraint(fields=['award_id', 'user_id'], name='uniq_award_user'),
        ]


class HackathonUserEnrol(models.Model):
    hack_id = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "hackathon_user_enrol"
        constraints = [
            models.UniqueConstraint(fields=['hack_id', 'user_id'], name='uniq_hack_user'),
        ]
