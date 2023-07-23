from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from hackathon.models import Hackathon, HackathonTeamEnrol, HackathonUserEnrol
from hackathon.serializers import HackathonCreateSerializer, HackathonEnrolTeamCreateSerializer, \
    HackathonEnrolUserCreateSerializer
from hacks.authentication import IsAdminPost, TokenAuthentication
from team.models import Team


class HackathonEnrolTeamCreateListView(generics.CreateAPIView, generics.ListAPIView, generics.UpdateAPIView):
    queryset = HackathonTeamEnrol.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = HackathonEnrolTeamCreateSerializer
    authentication_classes = [
        TokenAuthentication]

    def get_object(self):
        hack = Hackathon.objects.get(pk=self.kwargs['hack_id'])
        team_name = self.kwargs.get('team_name')
        team = Team.objects.filter(team_name=team_name).first()
        return HackathonTeamEnrol.objects.filter(hackathon=hack, team=team).first()

    def get_queryset(self):
        hack = Hackathon.objects.get(pk=self.kwargs['hack_id'])
        team_name = self.kwargs.get('team_name')
        if team_name:
            team = Team.objects.filter(team_name=team_name).first()
            return HackathonTeamEnrol.objects.filter(hackathon=hack, team=team)
        else:
            return HackathonTeamEnrol.objects.filter(hackathon=hack)


class HackathonEnrolUserCreateListView(generics.CreateAPIView):
    queryset = HackathonUserEnrol.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = HackathonEnrolUserCreateSerializer
    authentication_classes = [
        TokenAuthentication]

    def get_queryset(self):
        hack = Hackathon.objects.get(pk=self.kwargs['hack_id'])
        return HackathonUserEnrol.objects.filter(hackathon=hack)


class HackathonCreateListView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Hackathon.objects.all()
    permission_classes = (IsAdminPost,)
    serializer_class = HackathonCreateSerializer
    authentication_classes = [
        TokenAuthentication]

