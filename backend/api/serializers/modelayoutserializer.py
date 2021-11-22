from rest_framework import serializers
from api.serializers.ledprogramsserializer import LedProgramsSerializer

class ModeLayoutSerializer(serializers.Serializer):  
    
    modeId = serializers.IntegerField()
    modes = LedProgramsSerializer(many=True)
    minSpeed = serializers.IntegerField()
    maxSpeed = serializers.IntegerField()