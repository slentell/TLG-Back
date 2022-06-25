from numpy import maximum
from rest_framework import serializers
from .models import ImageGallery, Posts, Team, Athlete, MaxLift, LiftHistory
from django.db.models import Max
from auth_app.models import UserAccount

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'team_name', 'coach', 'primary_color', 'secondary_color', 'gender')
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

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bellRinger = False
        

    class Meta:
        fields = ('athlete', 'lift', 'weight', 'date_of_lift')
        model = LiftHistory
        
    def create(self, validated_data):

        maxLift = self.getMax(validated_data)
        lift, created = LiftHistory.objects.get_or_create(**validated_data)
        self.checkIfNewMax(lift, maxLift)

        return lift

    def getMax(self, validated_data):

        history = LiftHistory.objects.filter(athlete=validated_data['athlete'].id) 
        historyByLift = history.filter(lift=validated_data['lift'])
        maxLift = historyByLift.aggregate(Max('weight'))
        if maxLift['weight__max'] == None:
            maxLift['weight__max'] = 0
        return maxLift

    def checkIfNewMax(self, lift, maxLift):

        if maxLift['weight__max'] < lift.weight:
            
            try:
                userMaxes = MaxLift.objects.filter(athlete=lift.athlete.pk)
                userLiftMax = userMaxes.get(max_lift__lift=lift.lift)
                userLiftMax.max_lift = lift
                userLiftMax.save()
                self.bellRinger = True
                return True
            
            except:
                MaxLift.objects.create(athlete=lift.athlete, max_lift=lift)
                self.bellRinger = True
                return True
        else:
            self.bellRinger = False
            return False

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'content', 'image', 'author', 'date')
        model = Posts

class ImageGallerySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('author', 'image')
        model = ImageGallery
    