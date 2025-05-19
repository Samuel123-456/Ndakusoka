from django.urls import path
from course.views import (
      viewCourses,
      viewCourseSingle,
      comment,
      remove_comment
)

urlpatterns = [
      path('', viewCourses, name='course'),
      path('comment/', comment, name='comment'),
      path('remove/<int:id>', remove_comment, name='remove-comment'),
      path('course-single/<slug:slug>', viewCourseSingle, name='course_single')
]