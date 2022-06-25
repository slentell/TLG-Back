from rest_framework import generics, viewsets, response
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import ImageGallery, Posts, Team, Athlete, LiftHistory, MaxLift
from .serializers import ImageGallerySerializer, PostSerializer, TeamSerializer, AthleteSerializer, LiftHistorySerializer, MaxLiftSerializer


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
            serializer = serializer_class(data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({'status' : 'ok'}, status = 200)
            else:
                return Response({'error' : serializer.errors}, status=400 )
                
class AthleteViewSet(viewsets.ModelViewSet):
    queryset = Athlete.objects.all()
    serializer_class = AthleteSerializer
    http_method_names = ['get', 'post', 'put', 'options', 'delete',]

class LiftHistoryViewSet(viewsets.ModelViewSet):
    queryset = LiftHistory.objects.all()
    serializer_class = LiftHistorySerializer
    http_method_names = ['get', 'post', 'options', 'put', 'delete',]

    def create(self, request):

            serializer_class = LiftHistorySerializer
            if self.request.method == "POST":
                # athlete = self.request.user.pk
                athlete = 2
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
        queryset = LiftHistory.objects.filter(athlete__athlete=pk)
        serializer = LiftHistorySerializer(queryset, many=True)

        return response.Response(serializer.data)

class MaxLiftViewSet(viewsets.ModelViewSet):
    queryset = MaxLift.objects.all()
    serializer_class = MaxLiftSerializer
    http_method_names = ['get', 'post', 'options', 'put','delete',]

class ImageGalleryViewSet(viewsets.ModelViewSet):
    queryset = ImageGallery.objects.all()
    serializer_class = ImageGallerySerializer
    http_method_names = ['get', 'post', 'options', 'put','delete',]

# class PostsViewSet(viewsets.ModelViewSet):
#     queryset = Posts.objects.all()
#     serializer_class = PostSerializer
#     http_method_names = ['get', 'post', 'options', 'put','delete',]



