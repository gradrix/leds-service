from django.urls import re_path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

router = routers.SimpleRouter()

urlpatterns = [
    re_path(r'^status/', views.LedStatusView.as_view()),
    re_path(r'^layout/', views.ModeLayoutView.as_view()),    
    re_path(r'^changestatus/', views.LedStatusSetView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
