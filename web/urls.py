from django.urls import path
from web.views import (
      teachers,
      course,
      home,
)

urlpatterns = [
      path('home/', home, name='home'),
      path('teacher/', teachers, name='teachers'),
      path('course/', course, name='course'),
      
]
