from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import generics, authentication, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from hacks.authentication import TokenAuthentication
from team.models import Team
from team.serializers import TeamCreateSerializer


class TeamCreateListView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Team.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = TeamCreateSerializer
    authentication_classes = [
        TokenAuthentication]

    def get_queryset(self):
        return Team.objects.all().filter(owner_user_id=self.request.user)

