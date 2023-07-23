# Generated by Django 4.2.3 on 2023-07-23 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackathon', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='hackathonteamenrol',
            constraint=models.UniqueConstraint(fields=('hackathon', 'team'), name='uniq_hackathon_team'),
        ),
    ]