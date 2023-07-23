from django.contrib.auth.models import User
from rest_framework import serializers

from user.enums import DevType
from user.models import Profile


class ProfileCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    description = serializers.CharField()
    pfp_url = serializers.CharField()
    dev_type = serializers.IntegerField()

    class Meta:
        model = Profile
        fields = ("user", "description", "pfp_url", "dev_type")

    def validate(self, data):
        logged_in_username = self.context['request'].user.username
        requested_username = self.context['view'].kwargs['username']

        if self.context['request'].method in ['POST', 'PATCH'] and \
                not self.context['request'].user.is_staff and \
                logged_in_username != requested_username:
            raise serializers.ValidationError("You are not permitted to edit this user profile")

        if not DevType(data['dev_type']):
            raise serializers.ValidationError("Unknown dev_type")

        return data

    def create(self, validated_data):
        user = User.objects.get(username=self.context['view'].kwargs['username'])

        profile = Profile.objects.create(
            user=user,
            description=validated_data['description'],
            pfp_url=validated_data['pfp_url'],
            dev_type=validated_data['dev_type']
        )
        profile.save()
        return profile

    def update(self, instance, validated_data):
        instance.description = validated_data['description']
        instance.pfp_url = validated_data['pfp_url']
        instance.dev_type = validated_data['dev_type']
        instance.save()
        return instance
