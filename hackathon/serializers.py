from django.contrib.auth.models import User
from rest_framework import serializers

from hackathon.models import Hackathon, HackathonTeamEnrol, HackathonUserEnrol
from team.models import Team, TeamMembership


class HackathonEnrolTeamCreateSerializer(serializers.ModelSerializer):
    hackathon = serializers.PrimaryKeyRelatedField(read_only=True)
    team = serializers.CharField(read_only=True)
    project_name = serializers.CharField(required=False, allow_null=True)
    project_description = serializers.CharField(required=False, allow_null=True)
    project_presentation_url = serializers.CharField(required=False, allow_null=True)
    project_code_url = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = HackathonTeamEnrol
        fields = ("hackathon", "team", "project_name", "project_description",
                  "project_presentation_url", "project_code_url")

    def validate(self, data):
        hackathon = Hackathon.objects.get(pk=self.context['view'].kwargs['hack_id'])
        team = Team.objects.get(team_name=self.context['view'].kwargs['team_name'])
        if team.owner.id != self.context['request'].user.id:
            raise serializers.ValidationError("You are not the owner of this team")

        if self.context['request'].method == 'POST' and \
                HackathonTeamEnrol.objects.filter(team=team, hackathon=hackathon).exists():
            raise serializers.ValidationError("This team is already enrolled")

        return data

    def create(self, validated_data):
        team_enrol = HackathonTeamEnrol.objects.create(
            hackathon=Hackathon.objects.get(pk=self.context['view'].kwargs['hack_id']),
            team=Team.objects.get(team_name=self.context['view'].kwargs['team_name'])
        )
        team_enrol.save()
        return team_enrol

    def update(self, instance, validated_data):
        instance.project_name = validated_data['project_name']
        instance.project_description = validated_data['project_description']
        instance.project_presentation_url = validated_data['project_presentation_url']
        instance.project_code_url = validated_data['project_code_url']
        instance.save()
        return instance


class HackathonEnrolUserCreateSerializer(serializers.ModelSerializer):
    hackathon = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.CharField(read_only=True)

    class Meta:
        model = HackathonUserEnrol
        fields = ("hackathon", "user")

    def validate(self, data):
        hackathon = Hackathon.objects.get(pk=self.context['view'].kwargs['hack_id'])
        user = User.objects.get(pk=self.context['request'].user.id)
        user_teams = [tm.team for tm in TeamMembership.objects.filter(user=user)]
        hackathon_teams = [te.team for te in HackathonTeamEnrol.objects.filter(hackathon=hackathon)]
        for user_team in user_teams:
            if user_team in hackathon_teams:
                raise serializers.ValidationError(f"You are already registered through team {user_team}")

        return data


    def create(self, validated_data):
        user = User.objects.get(pk=self.context['request'].user.id)
        user_enrol = HackathonUserEnrol.objects.create(
            hackathon=Hackathon.objects.get(pk=self.context['view'].kwargs['hack_id']),
            user=user
        )
        user_enrol.save()
        return user_enrol


class HackathonCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    start_date = serializers.DateTimeField(required=True)
    end_date = serializers.DateTimeField(required=True)

    class Meta:
        model = Hackathon
        fields = "__all__"

    def create(self, validated_data):
        team = Hackathon.objects.create(
            name=validated_data['name'],
            description=validated_data['description'],
            start_date=validated_data['start_date'],
            end_date=validated_data['end_date']
        )

        team.save()

        return team