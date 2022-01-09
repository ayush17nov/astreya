from django.urls import path
from django.urls.conf import re_path
from django.urls import path
from .views import index, home, start_game


app_name = "game"

urlpatterns = [
    path('', index, name="index"),
    path('game/home/', home, name="home"),
    re_path(r'game/home/(?P<user_choice>\w+)$',start_game, name='start_game'),
]