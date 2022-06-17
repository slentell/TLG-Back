from rest_framework import serializers
from .models import Posts, Team, Athlete, MaxLift, LiftHistory


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('team_name', 'coach', 'primary_color', 'secondary_color', 'gender')
        model = Team

class AthleteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('athlete', 'grade', 'gender', 'weight', 'dob', 'team', 'weightclass')
        model = Athlete

class MaxLiftSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('athlete', 'max_lift')
        model = MaxLift

class LiftHistorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('athlete', 'lift', 'weight', 'date_of_lift')
        model = LiftHistory

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'content', 'image')
        model = Posts