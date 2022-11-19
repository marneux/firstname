from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .models import Vote, Firstname
from .views import VoteViewSet, HistoryViewSet, FirstnameViewSet

router = DefaultRouter()
router.register('votes', VoteViewSet, 'vote')
router.register('history', HistoryViewSet, 'history')
router.register('firstnames', FirstnameViewSet, 'firstname')

urlpatterns = [
  path('', include(router.urls)),
]
