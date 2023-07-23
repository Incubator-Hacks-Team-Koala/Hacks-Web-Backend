from django.urls import path

from user.views import ProfileCreateListView

urlpatterns = [
    path('<str:username>/profile', ProfileCreateListView.as_view(), name='user_profile')
]
