from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import generics, authentication, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from hacks.authentication import TokenAuthentication
from team.models import Team
from team.serializers import TeamCreateSerializer, TeamJoinSerializer


class TeamJoinView(generics.CreateAPIView):
    queryset = Team.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = TeamJoinSerializer
    authentication_classes = [
        TokenAuthentication]


class TeamCreateListView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Team.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = TeamCreateSerializer
    authentication_classes = [
        TokenAuthentication]

    def get_queryset(self):
        if self.kwargs['team_name']:
            return Team.objects.all().filter(team_name=self.kwargs['team_name'])
        else:
            return Team.objects.all().filter(owner=User.objects.get(pk=self.request.user.id))

