import re

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from team.models import Team, TeamMembership


class TeamJoinSerializer(serializers.ModelSerializer):
    team = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    passcode = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        team = Team.objects.all().filter(team_name=self.context['view'].kwargs['team_name'])
        if not team:
            raise serializers.ValidationError("Team does not exist")

        if team[0].passcode != data['passcode']:
            raise serializers.ValidationError("Passcode is not correct")
        return data

    class Meta:
        model = Team
        # fields = ('team_name', 'description', 'passcode')
        fields = ("team", "user", "passcode")

    def create(self, validated_data):
        team = Team.objects.filter(team_name=self.context['view'].kwargs['team_name']).first()
        user = User.objects.get(pk=self.context['request'].user.id)
        enrol = TeamMembership.objects.create(
            team=team,
            user=user
        )

        return enrol



class TeamCreateSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(read_only=True,
                                      validators=[UniqueValidator(queryset=Team.objects.all())])
    description = serializers.CharField(required=True)
    owner = serializers.CharField(read_only=True)
    team_name_pretty = serializers.CharField(required=True)
    passcode = serializers.CharField(required=False)


    class Meta:
        model = Team
        fields = ('team_name', 'description', 'passcode', 'owner', 'team_name_pretty')

    def validate(self, data):
        if not re.compile('^[a-zA-Z0-9_. ]+$').match(data['team_name_pretty']):
            raise serializers.ValidationError(
                "Invalid team_name_pretty, characters must be alphanumeric, space, period or underscore")

        data['team_name'] = data['team_name_pretty'].lower().replace(" ", "_")

        if Team.objects.filter(team_name=data['team_name']).exists():
            raise serializers.ValidationError(
                "Invalid team_name_pretty, That team name already exists")

        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        team = instance
        user = User.objects.get(pk=self.context['request'].user.id)
        if not TeamMembership.objects.filter(user=user, team=team).exists():
            representation.pop('passcode')

        return representation


    def create(self, validated_data):
        team = Team.objects.create(
            team_name=validated_data['team_name'],
            description=validated_data['description'],
            passcode=validated_data['passcode'],
            owner=User.objects.get(pk=self.context['request'].user.id),
            team_name_pretty=validated_data['team_name_pretty']
        )

        team.save()

        return team

    # def update(self, instance, validated_data):
    #     return validated_data
