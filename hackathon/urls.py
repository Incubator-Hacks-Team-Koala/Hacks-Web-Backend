from django.urls import path

from hackathon.views import HackathonCreateListView, HackathonEnrolTeamCreateListView, HackathonEnrolUserCreateListView, \
    HackathonAwardCreateListView, HackathonAwardVoteView, HackathonGroupUserCreateView

urlpatterns = [
    path('hackathon/<int:hack_id>/team/<str:team_name>/enrol', HackathonEnrolTeamCreateListView.as_view(),
         name='hackathon_team'),
    path('hackathon/<int:hack_id>/team/<str:team_name>', HackathonEnrolTeamCreateListView.as_view(),
         name='hackathon_team'),
    path('hackathon/<int:hack_id>/team', HackathonEnrolTeamCreateListView.as_view(),
         name='hackathon_team'),
    path('hackathon/<int:hack_id>/user/enrol', HackathonEnrolUserCreateListView.as_view(),
         name='hackathon_user_enrol'),
    path('hackathon/<int:hack_id>/user/group', HackathonGroupUserCreateView.as_view(),
         name='hackathon_user_enrol'),
    path('hackathon/<int:hack_id>/award/<int:award_id>/vote', HackathonAwardVoteView.as_view(),
         name='hackathon_award_vote'),
    path('hackathon/<int:hack_id>/award', HackathonAwardCreateListView.as_view(),
         name='hackathon_award'),
    path('hackathon', HackathonCreateListView.as_view(),
         name='hackathon')
]
