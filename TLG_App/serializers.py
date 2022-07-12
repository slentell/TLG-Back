from dataclasses import fields
from numpy import maximum
from rest_framework import serializers
from .models import Calendar, ImageGallery, Posts, Team, Athlete, MaxLift, LiftHistory
from django.db.models import Max
from auth_app.models import UserAccount
from auth_app.serializer import UserCreateSerializer

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'team_name', 'coach', 'primary_color', 'secondary_color', 'gender')
        model = Team

class AthleteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id','athlete', 'grade', 'gender', 'weight', 'dob', 'team', 'weightclass')

        model = Athlete

        def update(self, instance, validated_data):
            instance.id = validated_data.get('id', instance.id)
            instance.athlete = validated_data.get('athlete', instance.athlete)
            instance.grade = validated_data.get('grade', instance.grade)
            instance.gender = validated_data.get('gender', instance.gender)
            instance.weight = validated_data.get('weight', instance.weight)
            instance.dob = validated_data.get('dob', instance.dob)
            instance.weightclass = validated_data.get('weightclass', instance.weightclass)
            instance.save()
            return instance

class AthleteByTeamSerializer(serializers.ModelSerializer):
    athlete = UserCreateSerializer(many=False)
    team = TeamSerializer(many=False)
    class Meta:
        fields = ('athlete', 'grade', 'gender', 'weight', 'dob', 'team', 'weightclass', 'profile_picture')
        model = Athlete


class LiftHistorySerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bellRinger = False
        

    class Meta:
        fields = ('id', 'athlete', 'lift', 'weight', 'date_of_lift')
        model = LiftHistory
        
    def create(self, validated_data):
        print('inside create')
        maxLift = self.getMax(validated_data)
        lift, created = LiftHistory.objects.get_or_create(**validated_data)
        self.checkIfNewMax(lift, maxLift)

        return lift
        
    def update(self, instance, validated_data):
        print('inside serializer update', instance)
        print('validated data', validated_data)
        print('instance id ', instance.id)
        instance.id = validated_data.get('id', instance.id)
        instance.athlete = validated_data.get('athlete', instance.athlete)
        instance.lift = validated_data.get('lift', instance.lift)
        instance.date_of_lift = validated_data.get('date_of_lift', instance.date_of_lift)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.save()
        return instance

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

class MaxLiftByTeamSerializer(serializers.ModelSerializer):
    athlete = UserCreateSerializer()
    max_lift = LiftHistorySerializer()
    class Meta:
        fields = ('athlete', 'max_lift')
        model = MaxLift



class PostSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'content', 'image', 'author', 'date')
        model = Posts

class ImageGallerySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('author', 'image')
        model = ImageGallery
    
class CalendarSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'start', 'end', 'color', 'content', 'team')
        model = Calendar