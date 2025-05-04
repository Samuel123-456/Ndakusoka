from django.shortcuts import render
from django.views import View
from course.models import Course, Module
from datetime import timedelta

# Create your views here.
class CourseView(View):
      def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.template_name = 'web/course.html'
            
      def get(self, request):
            ctx = {}
            courses = Course.objects.all()
            ctx['courses'] = courses


            return render(request, self.template_name, ctx)


#def course(request):
#      template_name = 'web/course.html'
#      ctx = {}

#      return render(request, template_name, ctx)