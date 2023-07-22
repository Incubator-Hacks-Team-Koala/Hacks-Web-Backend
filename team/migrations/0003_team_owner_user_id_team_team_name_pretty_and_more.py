# Generated by Django 4.2.3 on 2023-07-22 23:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('team', '0002_remove_team_id_alter_team_team_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='owner_user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='team_name_pretty',
            field=models.CharField(default='name', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='team',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='team',
            name='passcode',
            field=models.CharField(max_length=50),
        ),
        migrations.CreateModel(
            name='TeamMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.team')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='teammembership',
            constraint=models.UniqueConstraint(fields=('user_id', 'team_name'), name='uniq_user_team'),
        ),
    ]