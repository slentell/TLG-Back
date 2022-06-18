from rest_framework import generics, viewsets, response
from .models import Posts, Team, Athlete, LiftHistory, MaxLift
from .serializers import PostSerializer, TeamSerializer, AthleteSerializer, LiftHistorySerializer, MaxLiftSerializer

class PostList(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    def create(self, request):
        serializer = self.get_serializer(
        data = {
            'author': request.user.pk,
            'title': request.data['title'], 
            'content': request.data['content'],
            'image': request.data['image'] ,
        })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return response.Response(serializer.data)

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

class PostsViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    http_method_names = ['get', 'post', 'options', 'put','delete',]



