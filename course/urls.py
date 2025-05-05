from django.urls import path
from course.views import (
      viewCourses,
      viewCourseSingle,
)

urlpatterns = [
      path('', viewCourses, name='course'),
      path('course-single/<slug:slug>', viewCourseSingle, name='course_single')
]