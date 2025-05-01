from django.urls import path
from web.views import (
      teachers,
      home,
)

urlpatterns = [
      path('home/', home, name='home'),
      path('teacher/', teachers, name='teachers'),
    
]
