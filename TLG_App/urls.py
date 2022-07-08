from django.urls import path
from rest_framework import routers
from .views import CalendarViewSet, ImageGalleryViewSet, TeamViewSet, AthleteViewSet, LiftHistoryViewSet, MaxLiftByTeamViewSet, PostsViewSet, AthleteByTeamViewSet, DevinStoleMyShitViewSet

router = routers.DefaultRouter()
router.register(r'team', TeamViewSet)
router.register(r'athlete', AthleteViewSet)
router.register(r'lift-history', LiftHistoryViewSet)
router.register(r'max-lift-by-team', MaxLiftByTeamViewSet, basename='max-lift-by-team')
router.register(r'posts', PostsViewSet)
router.register(r'image-gallery', ImageGalleryViewSet),
router.register(r'athlete-by-team', AthleteByTeamViewSet, 
basename='athlete-by-team' )
router.register(r'bell-ringer-by-team', DevinStoleMyShitViewSet, basename='bell-ringer-by-team'), 
router.register(r'calendar', CalendarViewSet), 




urlpatterns = router.urls
# [
#     path('test/', test_view),
#     path('', PostList.as_view()),
# ]