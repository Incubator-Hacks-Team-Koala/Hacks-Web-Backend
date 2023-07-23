from django.urls import path

from hackathon.views import HackathonCreateListView

urlpatterns = [
    path('hackathon', HackathonCreateListView.as_view(), name='hackathon')
]
