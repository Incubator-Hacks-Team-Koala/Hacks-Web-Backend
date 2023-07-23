from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from hackathon.models import Hackathon, HackathonTeamEnrol, HackathonUserEnrol, HackathonAward
from hackathon.serializers import HackathonCreateSerializer, HackathonEnrolTeamCreateSerializer, \
    HackathonEnrolUserCreateSerializer, HackathonAwardCreateSerializer, HackathonAwardVoteSerializer, \
    HackathonGroupUserCreateSerializer
from hacks.authentication import TokenAuthentication, AllowAnyGet
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

class HackathonGroupUserCreateView(generics.CreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = HackathonGroupUserCreateSerializer
    authentication_classes = [
        TokenAuthentication]



class HackathonCreateListView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Hackathon.objects.all()
    permission_classes = [AllowAnyGet | IsAdminUser]
    serializer_class = HackathonCreateSerializer
    authentication_classes = [
        TokenAuthentication]


class HackathonAwardCreateListView(generics.CreateAPIView, generics.ListAPIView):
    queryset = HackathonAward.objects.all()
    permission_classes = [AllowAnyGet | IsAdminUser]
    serializer_class = HackathonAwardCreateSerializer
    authentication_classes = [
        TokenAuthentication]

    def get_queryset(self):
        hack = Hackathon.objects.get(pk=self.kwargs['hack_id'])
        return HackathonAward.objects.filter(hackathon=hack)


class HackathonAwardVoteView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = HackathonAwardVoteSerializer
    authentication_classes = [
        TokenAuthentication]

