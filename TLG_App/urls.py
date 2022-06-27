from django.urls import path
from rest_framework import routers
from .views import ImageGalleryViewSet, TeamViewSet, AthleteViewSet, LiftHistoryViewSet, MaxLiftViewSet, PostsViewSet

router = routers.DefaultRouter()
router.register(r'team', TeamViewSet)
router.register(r'athlete', AthleteViewSet)
router.register(r'lift-history', LiftHistoryViewSet)
router.register(r'max-lift', MaxLiftViewSet)
router.register(r'posts', PostsViewSet)
router.register(r'image-gallery', ImageGalleryViewSet)




urlpatterns = router.urls
# [
#     path('test/', test_view),
#     path('', PostList.as_view()),
# ]