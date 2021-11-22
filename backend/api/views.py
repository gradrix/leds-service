from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from api.models.ledsettings import LedSettings
from api.models.modelayout import ModeLayout
from api.serializers.ledsettingsserializer import LedSettingsSerializer
from api.serializers.modelayoutserializer import ModeLayoutSerializer
from api.ledservicewrapper import LedServiceWrapper

class BaseView(APIView):

    authentication_classes = []

    class Meta:   
        abstract = True
        app_label = 'api'
        authentication_classes = []

    def __init__(self):
        self.ledSvc = LedServiceWrapper()

    def ledSettingsToJson(self, ledSettings):
        result = LedSettingsSerializer(ledSettings)
        return result.data

    def modeLayoutToJson(self, modeLayout):
        result = ModeLayoutSerializer(modeLayout)
        return result.data

    def setSetting(self, key, value):
        return self.ledSvc.setSetting(key + ":" +str(value))

    def has_permission(self, f, s):
        return True

class LedStatusView(BaseView):
               
    def get(self, request):
        try:
          result = self.ledSvc.getSettings() 
        except Exception as e:
          result = LedSettings()
        return Response(self.ledSettingsToJson(result))

class ModeLayoutView(BaseView):

    def get(self, request):
        try:
          result = self.ledSvc.getModeLayout()
        except Exception as e:
          result = ModeLayout()
        return Response(self.modeLayoutToJson(result))

class LedStatusSetView(BaseView):

    def post(self, request):
        result = None
        key = request.data["key"]
        value = request.data["value"]
        if (key == "brightness"):
            result = self.setSetting("B",value)
        elif (key == "isOn"):
            if (value):
                onValue = "1"
            else:
                onValue = "0"
            result = self.setSetting("O",onValue)
        elif (key == "mode"):
            result = self.setSetting("M",value)
        elif (key == "toggle"):
            result = self.setSetting("T",value)
        elif (key == "speed"):
            result = self.setSetting("S",value)
        elif (key == "color"):
            result = self.setSetting("C",value)

        return Response(self.ledSettingsToJson(result))
