from django.urls import path
from student.views import (
    enrollment
)

urlpatterns = [
    path('enrollment/<slug:slug>', enrollment, name='enrollment')
]
