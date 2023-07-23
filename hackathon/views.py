from django.shortcuts import render
from rest_framework import generics

from hackathon.models import Hackathon
from hackathon.serializers import HackathonCreateSerializer
from hacks.authentication import IsAuthenticatedGetIsAdminPost, TokenAuthentication


class HackathonCreateListView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Hackathon.objects.all()
    permission_classes = (IsAuthenticatedGetIsAdminPost,)
    serializer_class = HackathonCreateSerializer
    authentication_classes = [
        TokenAuthentication]

    def get_queryset(self):
        return Hackathon.objects.all()
