from django.urls import path
from course.views import (
      CourseView
)

urlpatterns = [
      path('', CourseView.as_view(), name='course'),
]
