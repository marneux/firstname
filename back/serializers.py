from doublemetaphone import doublemetaphone
import logging
from rest_framework import serializers

from .models import Vote, Firstname


logger = logging.getLogger(__name__)

class FirstnameSerializer(serializers.ModelSerializer):
  class Meta:
    model = Firstname
    fields = ('id', 'sex', 'firstname')

  def create(self, validated_data):
    validated_data['firstname'] = validated_data['firstname'].title()
    validated_data['sex'] = validated_data['sex'].upper()
    validated_data['metaphone'] = doublemetaphone(validated_data['firstname'])[0]
    return Firstname.objects.create(**validated_data)

class VoteSerializer(serializers.ModelSerializer):
  who = serializers.CharField(default=serializers.CurrentUserDefault())
  class Meta:
    model = Vote
    fields = '__all__'
    extra_kwargs = {
      'who': {'required': False},
    }

class HistorySerializer(serializers.ModelSerializer):
  who = serializers.CharField(default=serializers.CurrentUserDefault())
  firstname = FirstnameSerializer(read_only = True)
  modify_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", required=False, read_only=True)
  class Meta:
    model = Vote
    fields = '__all__'
    extra_kwargs = {
      'who': {'required': False},
    }
