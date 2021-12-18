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

    def setSetting(self, key, value, serviceIndex = 1):
        return self.ledSvc.setSetting(key + ":" +str(value), serviceIndex)

    def has_permission(self, f, s):
        return True

    def getServiceIndex(self, request):
        serviceIndex = 1
        if "serviceIndex" in request:
            try:
                serviceIndex = int(request["serviceIndex"])
            except:
                serviceIndex = 1
                print("Incorrect serviceIndex value passed")
        return serviceIndex

class LedStatusView(BaseView):
               
    def get(self, request):
        index = self.getServiceIndex(request.query_params)
        try:
            result = self.ledSvc.getSettings(None, index) 
        except Exception as e:
            print("Setting retrieval error!")
            result = LedSettings()

        result.service = index
        return Response(self.ledSettingsToJson(result))

class ModeLayoutView(BaseView):

    def get(self, request):
        index = self.getServiceIndex(request.query_params)
        try:
            result = self.ledSvc.getModeLayout(index)
        except Exception as e:
            result = ModeLayout()
        result.service = index
        return Response(self.modeLayoutToJson(result))

class LedStatusSetView(BaseView):

    def post(self, request):
        result = None
        index = self.getServiceIndex(request.data)
        key = request.data["key"]
        value = request.data["value"]
        if (key == "brightness"):
            result = self.setSetting("B",value, index)
        elif (key == "isOn"):
            if (value):
                onValue = "1"
            else:
                onValue = "0"
            result = self.setSetting("O",onValue, index)
        elif (key == "mode"):
            result = self.setSetting("M",value, index)
        elif (key == "toggle"):
            result = self.setSetting("T",value, index)
        elif (key == "speed"):
            result = self.setSetting("S",value, index)
        elif (key == "color"):
            result = self.setSetting("C",value, index)

        result.service = index
        return Response(self.ledSettingsToJson(result))
