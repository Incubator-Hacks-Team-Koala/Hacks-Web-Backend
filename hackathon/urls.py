from django.urls import path

from hackathon.views import HackathonCreateListView, HackathonEnrolTeamCreateListView, HackathonEnrolUserCreateListView

urlpatterns = [
    path('hackathon/<int:hack_id>/team/<str:team_name>/enrol', HackathonEnrolTeamCreateListView.as_view(), name='hackathon_team'),
    path('hackathon/<int:hack_id>/team/<str:team_name>', HackathonEnrolTeamCreateListView.as_view(), name='hackathon_team'),
    path('hackathon/<int:hack_id>/team', HackathonEnrolTeamCreateListView.as_view(), name='hackathon_team'),
    path('hackathon/<int:hack_id>/user/enrol', HackathonEnrolUserCreateListView.as_view(), name='hackathon_user_enrol'),
    path('hackathon', HackathonCreateListView.as_view(), name='hackathon')
]
