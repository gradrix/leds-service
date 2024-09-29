from pprint import pprint
from rest_framework import serializers
from api.models.ledprogram import LedProgram

class LedProgramsSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    name = serializers.StringRelatedField()