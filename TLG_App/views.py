from venv import create
from requests import request

from rest_framework import generics, viewsets, response
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import ImageGallery, Posts, Team, Athlete, LiftHistory, MaxLift, Calendar
from .serializers import AthleteByTeamSerializer, ImageGallerySerializer, PostSerializer, TeamSerializer, AthleteSerializer, LiftHistorySerializer, MaxLiftByTeamSerializer, CalendarSerializer
import json

def teamByCoach(coachUserId):
    team = Team.objects.get(coach=coachUserId)
    return team

class PostsViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    filterset_fields=['author']
    http_method_names = ['get', 'post', 'options', 'put','delete',]

    def create(self, request):
        serializer_class = PostSerializer

        if self.request.method == "POST":
            author = self.request.user.pk
            title = request.data.get('title')
            content = request.data.get('content')
            image = request.data.get('image')
    
            if image == '':
                image = None
            data = {
                'author': author,
                'title': title,
                'content': content,
                'image': image
            
            }
            serializer = serializer_class(data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({'status' : 'ok'}, status = 200)
            else:
                return Response({'error' : serializer.errors}, status=400 )
    

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    http_method_names = ['get', 'post', 'put', 'options', 'delete',]

    def create(self, request):
        serializer_class = TeamSerializer

        if self.request.method == "POST":
            coach = self.request.user.pk
            team_name = request.data.get('team_name')
            primary_color = request.data.get('primary_color')
            secondary_color = request.data.get('secondary_color')
            gender = request.data.get('gender')

            data = {
                'coach': coach,
                'team_name': team_name,
                'primary_color': primary_color,
                'secondary_color': secondary_color,
                'gender': gender
            }
            print(data)
            serializer = serializer_class(data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({'status' : 'ok'}, status = 200)
            else:
                return Response({'error' : serializer.errors}, status=400 )
    
    def get_queryset(self):
        coach_acct = self.request.user
        if coach_acct.account_type == 2:
            return Team.objects.filter(coach=coach_acct)
        return Team.objects.all()

class AthleteViewSet(viewsets.ModelViewSet):
    queryset = Athlete.objects.all()
    serializer_class = AthleteSerializer
    http_method_names = ['get', 'post', 'put', 'options', 'delete',]

    def create(self, request):
        serializer_class = AthleteSerializer

        if self.request.method == "POST":
            print("I'm here")
            print(self.request.user.pk)
            print(type(self.request.user.pk))
            athlete = self.request.user.pk

            grade = request.data.get('grade')
            gender = request.data.get('gender')
            dob = request.data.get('dob')
            weight = request.data.get('weight')
            team_id = request.data.get('team')
            weightclass = Athlete.return_weightclass(gender=gender, weight_input=weight)

            data = {
                'athlete' : athlete,
                'grade': grade,
                'gender': gender,
                'dob': dob,
                'weight': weight,
                'weightclass': weightclass,
                'team': team_id
            }
            print('data:',data)

            serializer = serializer_class(data=data, partial=True)
            print("got serialized")
            if serializer.is_valid():

                print("is valid")
                serializer.save()
                return Response({'status' : 'ok'}, status = 200)
            else:
                return Response({'error' : serializer.errors}, status=400 )


    def update(self, request, pk):
            print("I'm putting here")
            print(pk)
            print(type(pk))
            athlete_query = Athlete.objects.get(athlete=self.request.user.pk)
          
            athlete = self.request.user.pk

            grade = request.data.get('grade')
            gender = request.data.get('gender')
            dob = request.data.get('dob')
            weight = request.data.get('weight')
            team_id = request.data.get('team')
            weightclass = Athlete.return_weightclass(gender=gender, weight_input=weight)

            data = {
                'athlete' : athlete,
                'grade': grade,
                'gender': gender,
                'dob': dob,
                'weight': weight,
                'weightclass': weightclass,
                'team': team_id
            }
            print('data:',data)

            serializer = AthleteSerializer(athlete_query, data=data)
            print("got serialized")
            if serializer.is_valid():

                print("is valid")
                serializer.save()
                return Response({'status' : 'ok'}, status = 200)
            else:
                return Response({'error' : serializer.errors}, status=400 )

    def retrieve(self, request, pk):
        print('inside retrieve')
        queryset = Athlete.objects.get(athlete__id=pk)
        print('queryset ', queryset)
        serializer = AthleteByTeamSerializer(queryset, many=False)
        print('serialized ', serializer)
        return response.Response(serializer.data)


class AthleteByTeamViewSet(viewsets.ViewSet):

    def list(self, request):

        team_id = teamByCoach(request.user.pk)
        athletes = Athlete.objects.filter(team=team_id)
        serializer = AthleteByTeamSerializer(athletes, many=True)
        return Response(serializer.data)

class LiftHistoryViewSet(viewsets.ModelViewSet):
    queryset = LiftHistory.objects.all()
    serializer_class = LiftHistorySerializer
    http_method_names = ['get', 'post', 'options', 'put', 'delete',]

    def create(self, request):

            serializer_class = LiftHistorySerializer
            if self.request.method == "POST":
                athlete = self.request.user.pk
                lift = request.data.get('lift')
                weight = request.data.get('weight')
                date_of_lift = request.data.get('date_of_lift')

                data = {
                    'athlete': athlete,
                    'lift': lift,
                    'weight': weight,
                    'date_of_lift': date_of_lift,
                }
            
                serializer = serializer_class(data=data, partial=True)
                print(serializer)

                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'status' : 'ok',
                        'data' : serializer.data,
                        'bell ringer' : serializer.bellRinger
                        }, status = 200)
                else:
                    return Response({'error' : serializer.errors}, status=400 )

    def list(self, request):
        teamId = request.query_params['team']
        teamLifts = LiftHistory.objects.filter(athlete__athlete__team_id=teamId)
        serializer = LiftHistorySerializer(teamLifts, many=True)
        
        return response.Response(serializer.data)

    def retrieve(self, request, pk):
        print('inside retrieve ')
        queryset = LiftHistory.objects.filter(athlete__id=pk).order_by('date_of_lift')
        serializer = LiftHistorySerializer(queryset, many=True)
        return response.Response(serializer.data)

    def update(self, request, pk=None):
        print('inside update view', request.data, pk)
        print('id ', request.data.get('id'))
        lift_query = LiftHistory.objects.filter(athlete__id=pk).get(id=request.data.get('id'))
        print('liftQuery', lift_query)
        # liftQuery = LiftHistory.objects.filter(athlete__id=pk).get(id=request.data.get('id'))
        data = {
            'athlete': pk,
            'lift': request.data.get('lift'),
            'weight': request.data.get('weight'),
            'date_of_lift': request.data.get('date_of_lift'),
        }
        serializer = LiftHistorySerializer(lift_query, data=data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        else:
            return Response({'error' : serializer.errors}, status=400 )
    
    def destroy(self, request, pk=None):
        print('inside delete view')
        if request.method == 'DELETE':
            lift_object = LiftHistory.objects.filter(athlete__id=pk).get(id=request.data.get('id'))
            lift_object.delete()
            return Response({'status' : 'ok'}, status=200)
        else:
            return Response({'error' : 'error deleting'}, status=400)


class MaxLiftByTeamViewSet(viewsets.ViewSet):

    def list(self, request):
        try:
            teamId = teamByCoach(request.user.pk)
            print(teamId)
        except:
            athleteObj = Athlete.objects.get(athlete=request.user.pk)
            teamId = athleteObj.team_id
            print(teamId)
        teamLifts = MaxLift.objects.filter(athlete__athlete__team_id=teamId).order_by('id')
        serializer = MaxLiftByTeamSerializer(teamLifts, many=True)


        formatted_data = []

        record_created = False

        def create_record(name):
            return {'name': name}

        last = len(serializer.data)


        for idx in range(len(serializer.data)):
            name = serializer.data[idx]['athlete']['first_name'] + ' ' + serializer.data[idx]['athlete']['last_name']
        
            # if name not in dict add it then add lift data
            if not record_created:
                current_name = name
                athlete_max_row = create_record(name)
                record_created = True
            if current_name != name:
                formatted_data.append(athlete_max_row)
                current_name = name
                athlete_max_row = {}
                athlete_max_row = create_record(name)
            if current_name == name:
                athlete_max_row[serializer.data[idx]['max_lift']['lift']] = serializer.data[idx]['max_lift']['weight']
            if idx == last-1:
                formatted_data.append(athlete_max_row)
        
        return response.Response(formatted_data)

class DevinStoleMyShitViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            teamId = teamByCoach(request.user.pk)
            print(teamId)
        except:
            athleteObj = Athlete.objects.get(athlete=request.user.pk)
            teamId = athleteObj.team
            print(teamId)
        teamLifts = MaxLift.objects.filter(athlete__athlete__team_id=teamId)
        serializer = MaxLiftByTeamSerializer(teamLifts, many=True)
        return response.Response(serializer.data)

class ImageGalleryViewSet(viewsets.ModelViewSet):
    queryset = ImageGallery.objects.all()
    serializer_class = ImageGallerySerializer
    http_method_names = ['get', 'post', 'options', 'put','delete',]

    def create(self, request):
        print("LETS UPLOAD AN IMAGE")
        serializer_class = ImageGallerySerializer

        if self.request.method == "POST":
            author = self.request.user.pk
            image = request.data.get('image')

            data = {
                'author': author,
                'image': image
            }
            print(image)

            serializer = serializer_class(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({'status' : 'ok'}, status = 200)
            else:
                return Response({'error' : serializer.errors}, status=400 )

def getTeamId(request):
    try:
        teamId = teamByCoach(request.user.pk)
        
    except:
        athleteObj = Athlete.objects.get(athlete=request.user.pk)
        teamId = athleteObj.team
        
    return teamId

class CalendarViewSet(viewsets.ModelViewSet):

    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

    def list(self, request):
        teamId = getTeamId(request)
        teamCalendarEvents = Calendar.objects.filter(team=teamId)
        serializer = CalendarSerializer(teamCalendarEvents, many=True)
        return response.Response(serializer.data)

    def create(self, request):
        teamId = getTeamId(request)
        print(teamId)
        # print(request.data)
        # print(request.data['data'].get('title'))
        title = request.data['data'].get('title')
        start = request.data['data'].get('start')
        end = request.data['data'].get('end')
        color = request.data['data'].get('color')
        content = request.data['data'].get('content')
        data = {
            'title': title,
            'start': start,
            'end': end,
            'color': color,
            'content': content,
            'team': teamId.pk
        }
        print(data)

        serializer = CalendarSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'status' : 'ok',
                # 'data': Calendar.objects.filter(team=teamId)
                }, status = 200)
        else:
            return Response({'error' : serializer.errors}, status=400 )