from django.urls import path
from web.views import (
      teachers,
      contact,
      course,
      about,
      home,
)

urlpatterns = [
      path('teacher/', teachers, name='teachers'),
      path('contact/', contact, name='contact'),
      path('course/', course, name='course'),
      path('about/', about, name='about'),
      path('home/', home, name='home'),
]
