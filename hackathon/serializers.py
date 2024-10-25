import random

from django.contrib.auth.models import User
from rest_framework import serializers

from hackathon.models import Hackathon, HackathonTeamEnrol, HackathonUserEnrol, HackathonAward, HackathonAwardVote
from team.models import Team, TeamMembership
from user.models import Profile


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


class HackathonGroupUserCreateSerializer(serializers.Serializer):
    team_min = serializers.IntegerField(write_only=True, min_value=2)
    team_max = serializers.IntegerField(write_only=True, min_value=2)

    def validate(self, data):
        hackathon = Hackathon.objects.get(pk=self.context['view'].kwargs['hack_id'])
        enrolled_users = HackathonUserEnrol.objects.filter(hackathon=hackathon)
        if len(enrolled_users) < data['team_min']:
            raise serializers.ValidationError("Not enough signed up members to put into groups")
        return data


    def create(self, validated_data):
        hackathon = Hackathon.objects.get(pk=self.context['view'].kwargs['hack_id'])
        enrolled_users = HackathonUserEnrol.objects.filter(hackathon=hackathon)
        dev_types = {1:[],2:[],3:[]}
        for enrolled_user in enrolled_users:
            profile = Profile.objects.get(user=enrolled_user.user)
            dev_types[profile.dev_type].append(enrolled_user.user)

        diff = 999
        team_size = 0
        for i in range(validated_data['team_min'], validated_data['team_max']):
            if len(enrolled_users) % i < diff:
                diff = len(enrolled_users) % i
                team_size = i

        no_teams = len(enrolled_users) // team_size

        team_groups = []
        for i in range(no_teams):
            team_group = []
            for y in range(team_size):
                devs = []
                offset = -1
                while not devs:
                    offset += 1
                    devs = dev_types[((y+offset) % 3)+1]

                team_group.append(dev_types[((y+offset) % 3)+1].pop())
            team_groups.append(team_group)


        for group in team_groups:
            team = Team.objects.create(
                team_name=f"auto_team_{hackathon.id}.{group[0].id}",
                team_name_pretty=f"auto_team_{hackathon.id}.{group[0].id}",
                owner=group[0],
                description="",
                passcode=random.randint(1000,999999)
            )

            for user in group:
                TeamMembership.objects.create(
                    team=team,
                    user=user
                )

            HackathonTeamEnrol.objects.create(
                team=team,
                hackathon=hackathon
            )

        # for enrolled_user in enrolled_users:
        #     enrolled_user.delete()

        return {"teams": [[user.username for user in team] for team in team_groups]}


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


class HackathonAwardCreateSerializer(serializers.ModelSerializer):
    hackathon = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    open_date = serializers.DateTimeField(required=True)
    close_date = serializers.DateTimeField(required=True)
    winner_team = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = HackathonAward
        fields = "__all__"

    def create(self, validated_data):
        hackathon = Hackathon.objects.get(pk=self.context['view'].kwargs['hack_id'])
        award = HackathonAward.objects.create(
            hackathon=hackathon,
            name=validated_data['name'],
            description=validated_data['description'],
            open_date=validated_data['open_date'],
            close_date=validated_data['close_date']
        )

        award.save()

        return award


class HackathonAwardVoteSerializer(serializers.ModelSerializer):
    award = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    user = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    team = serializers.CharField(required=True)

    class Meta:
        model = HackathonAwardVote
        fields = ("award", "user", "team")

    def validate(self, data):
        team = Team.objects.filter(team_name=data['team']).first()
        award = HackathonAward.objects.filter(pk=self.context['view'].kwargs['award_id']).first()
        user = User.objects.get(pk=self.context['request'].user.id)
        if not team:
            raise serializers.ValidationError("Unknown team")

        if not award:
            raise serializers.ValidationError("Unknown award")

        user_teams = [tm.team for tm in TeamMembership.objects.filter(user=user)]
        if team in user_teams:
            raise serializers.ValidationError("You cannot vote for your own team")

        if HackathonAwardVote.objects.filter(award=award,user=user).exists():
            raise serializers.ValidationError("You have already voted for this award")

        return data

    def create(self, validated_data):
        user = User.objects.get(pk=self.context['request'].user.id)
        award = HackathonAward.objects.get(pk=self.context['view'].kwargs['award_id'])
        team = Team.objects.get(team_name=validated_data['team'])
        award_vote = HackathonAwardVote.objects.create(
            award=award,
            user=user,
            team=team
        )

        award_vote.save()

        return award_vote
