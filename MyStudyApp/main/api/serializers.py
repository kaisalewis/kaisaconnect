from main.models import Room
from rest_framework.serializers import ModelSerializer
from main import models

class RoomSerializer(ModelSerializer):
     class Meta:
         model = Room
         fields = '__all__'