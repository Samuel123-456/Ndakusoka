from django.urls import path
from student.views import (
    enrollment
)

urlpatterns = [
    path('enrollment/', enrollment, name='enrollment')
]
