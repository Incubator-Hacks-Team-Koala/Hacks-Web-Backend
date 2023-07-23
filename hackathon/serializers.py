from rest_framework import serializers

from hackathon.models import Hackathon


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