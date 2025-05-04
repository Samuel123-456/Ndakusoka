from django.urls import path
from web.views import (
      teachers,
      contact,
      about,
      home,
)

urlpatterns = [
      path('teacher/', teachers, name='teachers'),
      path('contact/', contact, name='contact'),
      path('about/', about, name='about'),
      path('', home, name='home'),
]
