from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from hacks.authentication import TokenAuthentication
from user.models import Profile
from user.serializers import ProfileCreateSerializer


class ProfileCreateListView(generics.CreateAPIView, generics.RetrieveAPIView, generics.UpdateAPIView):
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileCreateSerializer
    authentication_classes = [
        TokenAuthentication]

    def get_object(self):
        user = User.objects.get(username=self.kwargs['username'])
        return Profile.objects.get(user=user)
