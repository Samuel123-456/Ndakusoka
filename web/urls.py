from django.urls import path
from web.views import (
      teachers,
      contact,
      home,
      AboutTemplateView
)

urlpatterns = [
      path('teacher/', teachers, name='teachers'),
      path('contact/', contact, name='contact'),
      path('about/', AboutTemplateView.as_view(), name='about'),
      path('', home, name='home'),
]
