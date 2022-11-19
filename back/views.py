import logging
from django.shortcuts import render, get_object_or_404
from django.db.models import Subquery
from rest_framework import viewsets
from rest_framework.views  import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination

from .models import Vote, Firstname
from .serializers import VoteSerializer, HistorySerializer, FirstnameSerializer

logger = logging.getLogger(__name__)


class StandardResultsSetPagination(PageNumberPagination):
  page_size = 100
  page_size_query_param = 'page_size'
  max_page_size = 1000
  
  def get_paginated_response(self, data):
    return Response(data)

class VoteViewSet(viewsets.ModelViewSet):
  serializer_class = VoteSerializer
  queryset = Vote.objects.all()
  pagination_class = StandardResultsSetPagination
  permission_classes = [IsAuthenticated]

  def get_serializer(self, *args, **kwargs):
    if isinstance(kwargs.get('data', {}), list):
      kwargs['many'] = True
    return super().get_serializer(*args, **kwargs)

class HistoryViewSet(viewsets.ModelViewSet):
  serializer_class = HistorySerializer
  queryset = Vote.objects.all()
  pagination_class = StandardResultsSetPagination
  permission_classes = [IsAuthenticated]

  def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        vote = get_object_or_404(queryset, pk=pk)
        logger.info(vote)
        serializer = VoteSerializer(vote)
        return Response(serializer.data)

  def list(self, request):
    page = self.paginator.paginate_queryset(Vote.objects.filter(who = request.user).order_by('-modify_at'), request)

    serializer = self.get_serializer(page, many = True)

    return self.paginator.get_paginated_response(serializer.data)

  @action(detail=True, methods=['patch'])
  def change_vote(self, request, pk = None):
    queryset = Vote.objects.all()
    vote = get_object_or_404(queryset, pk=pk)
    logger.info(vote)
    vote.choice = not vote.choice
    logger.info(vote)
    vote.save()
    serializer = VoteSerializer(vote)
    return Response(serializer.data)

class FirstnameViewSet(viewsets.ModelViewSet):
  serializer_class = FirstnameSerializer
  queryset = Firstname.objects.all()
  permission_classes = [IsAuthenticated]

  @action(detail=False)
  def metaphones(self, request):
    logger.info(request.query_params)
    sex = 'M'
    limit = 20
    if 'sex' in request.query_params:
      sex = request.query_params['sex']
    if 'limit' in request.query_params:
      limit = int(request.query_params['limit'])
    already_voted = Subquery(Vote.objects.values('firstname_id').filter(who = request.user.pk))
    metaphone = Subquery(Firstname.objects.values('metaphone').distinct().exclude(pk__in = already_voted).filter(sex = sex).order_by('metaphone')[:limit])
    data = Firstname.objects.exclude(pk__in = already_voted).filter(metaphone__in = metaphone).filter(sex = sex)
    serializer = self.get_serializer(data, many = True)
    return Response(serializer.data)
