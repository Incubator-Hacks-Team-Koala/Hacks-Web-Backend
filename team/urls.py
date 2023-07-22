from django.urls import path

from auth.views import MyObtainTokenPairView, RegisterView
from rest_framework_simplejwt.views import TokenRefreshView

from team.views import TeamCreateListView

urlpatterns = [
    path('team', TeamCreateListView.as_view(), name='team_edit')
]
