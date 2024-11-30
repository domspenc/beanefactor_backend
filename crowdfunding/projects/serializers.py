from rest_framework import serializers
from django.apps import apps

class TreatPledgeSerializer(serializers.ModelSerializer):
  class Meta:
      model = apps.get_model('projects.TreatPledge')
      fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
  class Meta:
      model = apps.get_model('projects.Project')
      fields = '__all__'

class ProjectDetailSerializer(ProjectSerializer):
  treat_pledges = TreatPledgeSerializer(many=True, read_only=True)