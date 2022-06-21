from rest_framework import generics, viewsets, response
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Posts, Team, Athlete, LiftHistory, MaxLift
from .serializers import PostSerializer, TeamSerializer, AthleteSerializer, LiftHistorySerializer, MaxLiftSerializer
from datetime import date

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
            post_date = date.today()
            if image == '':
                image = None
            data = {
                'author': author,
                'title': title,
                'content': content,
                'image': image,
                'date' : post_date
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

class AthleteViewSet(viewsets.ModelViewSet):
    queryset = Athlete.objects.all()
    serializer_class = AthleteSerializer
    http_method_names = ['get', 'post', 'put', 'options', 'delete',]

class LiftHistoryViewSet(viewsets.ModelViewSet):
    queryset = LiftHistory.objects.all()
    serializer_class = LiftHistorySerializer
    http_method_names = ['get', 'post', 'options', 'put', 'delete',]

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

# class PostsViewSet(viewsets.ModelViewSet):
#     queryset = Posts.objects.all()
#     serializer_class = PostSerializer
#     http_method_names = ['get', 'post', 'options', 'put','delete',]



