from django.urls import path
from .views import GameUsersAPIView


urlpatterns = [
    path('', GameUsersAPIView.as_view(), name="game-users"),
]