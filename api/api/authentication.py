from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

class NoAuthentication(authentication.BaseAuthentication):
    def has_permission(self, a, b):
        return True
    
    def has_object_permission(self, a, b, c):
        return True

    def authenticate(self, request):
        user = User()
        return (user, None)
