from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from team.models import Team


class TeamCreateSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(required=True,
                                      validators=[UniqueValidator(queryset=Team.objects.all())])
    description = serializers.CharField(required=True)
    passcode = serializers.CharField(required=True)

    class Meta:
        model = Team
        fields = ('team_name', 'description', 'passcode')

    def create(self, validated_data):
        team = Team.objects.create(
            team_name=validated_data['team_name'],
            description=validated_data['description'],
            passcode=validated_data['passcode']
        )

        team.save()

        return team

    # def update(self, instance, validated_data):
    #     return validated_data
