from django.urls import path
from course.views import (
      viewCourses,
      viewCourseSingle,
      comment,
      remove_comment,
      watchCourse
)


urlpatterns = [
      path('', viewCourses, name='course'),
      path('comment/', comment, name='comment'),
      path('remove/<int:id>', remove_comment, name='remove-comment'),
      path('course-single/<slug:slug>', viewCourseSingle, name='course_single'),
      path('course-watch/<slug:slug>', watchCourse, name='watch')
]