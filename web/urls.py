from django.urls import path
from web.views import (
      teachers,
      contact,
      HomeTemplateView,
      AboutTemplateView
)

urlpatterns = [
      path('teacher/', teachers, name='teachers'),
      #path('c/', contact, name='contact'),
      path('about/', AboutTemplateView.as_view(), name='about'),
      path('', HomeTemplateView.as_view(), name='home'),
]
