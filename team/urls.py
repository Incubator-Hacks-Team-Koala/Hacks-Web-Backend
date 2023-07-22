from django.urls import path

from auth.views import MyObtainTokenPairView, RegisterView
from rest_framework_simplejwt.views import TokenRefreshView

from team.views import TeamCreateView

urlpatterns = [
    path('create', TeamCreateView.as_view(), name='team_create')
]
