from rest_framework import serializers

class LedSettingsSerializer(serializers.Serializer):
    
    isOn = serializers.BooleanField()
    brightness = serializers.IntegerField()
    mode = serializers.IntegerField()
    toggle = serializers.IntegerField()
    speed = serializers.IntegerField()
    color = serializers.CharField(default="", max_length=6)