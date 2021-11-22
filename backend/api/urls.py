from django.conf.urls import url, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

router = routers.SimpleRouter()

urlpatterns = [
    url(r'^status/', views.LedStatusView.as_view()),
    url(r'^layout/', views.ModeLayoutView.as_view()),    
    url(r'^changestatus/', views.LedStatusSetView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)