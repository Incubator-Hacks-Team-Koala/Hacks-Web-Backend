from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny

from team.models import Team
from team.serializers import TeamCreateSerializer


# Create your views here.
class TeamCreateView(generics.CreateAPIView):
    queryset = Team.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TeamCreateSerializer
