from django.urls import path
from course.views import (
      watchCourse,

      #CBV
      CourseListView,
      CourseDetailView,
      CommentHandler
)

app_name = 'course'

urlpatterns = [
      # Course
      path('list/', CourseListView.as_view(), name='list-course'),
      path('detail/<slug:slug>', CourseDetailView.as_view(), name='detail-course'),
      path('course-watch/<slug:slug>', watchCourse, name='watch'),
      
      # Comments
      path('comment/create/<slug:slug>', CommentHandler.create_comment, name='create-comment'),
      path('comment/delete/<int:id>/<slug:slug>', CommentHandler.delete_comment, name='delete-comment'),
]