from django.db.models import fields
from rest_framework import serializers
from .models import GameUser


class GameUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameUser
        fields = ["name"]
