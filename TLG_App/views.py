from rest_framework import generics
from .models import Posts
from .serializers import PostSerializer

class PostList(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

# Create your views here.
def test_view():
    pass

