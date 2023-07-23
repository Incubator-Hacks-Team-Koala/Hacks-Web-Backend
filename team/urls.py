from django.urls import path

from auth.views import MyObtainTokenPairView, RegisterView
from rest_framework_simplejwt.views import TokenRefreshView

from team.views import TeamCreateListView, TeamJoinView

urlpatterns = [
    path('team/<str:team_name>/join', TeamJoinView.as_view(), name='team_join'),
    path('team/<str:team_name>', TeamCreateListView.as_view(), name='team_edit'),
    path('team', TeamCreateListView.as_view(), name='team_edit')
]
