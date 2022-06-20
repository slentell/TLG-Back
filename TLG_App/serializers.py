from rest_framework import serializers
from .models import Posts, Team, Athlete, MaxLift, LiftHistory
from django.db.models import Max
from auth_app.models import UserAccount



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
        
    def create(self, validated_data):

        maxLift = self.getMax(validated_data)
        lift, created = LiftHistory.objects.get_or_create(**validated_data)
        maxObj = self.checkIfNewMax(lift, maxLift)
        lift.newBR = maxObj
        return lift

    def getMax(self, validated_data):

        history = LiftHistory.objects.filter(athlete=validated_data['athlete'].id) 
        historyByLift = history.filter(lift=validated_data['lift'])
        maxLift = historyByLift.aggregate(Max('weight'))
        return maxLift

    def checkIfNewMax(self, lift, maxLift):

        if maxLift['weight__max'] < lift.weight:
            update_values = {'max_lift' : lift}
            maxObj, created = MaxLift.objects.update_or_create(athlete = lift.athlete, defaults=update_values)
            return maxObj
        else:
            return None

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'content', 'image', 'author')
        model = Posts
     