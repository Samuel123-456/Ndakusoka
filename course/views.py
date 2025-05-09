from django.shortcuts import render, redirect
from course.models import (
      Course, 
      Module,
      Comment
)
from django.views import View

# Create your views here.
def viewCourses(request):
      if request.method == 'GET':
            template_name = 'course/course.html'
            ctx = {}

            ctx['courses'] = Course.objects.all()

            return render(request, template_name, ctx)

def viewCourseSingle(request, slug):
      template_name = 'course/single.html'
      ctx = {}

      course = Course.objects.filter(slug=slug)

      print(request)

      if not course.exists():
            return redirect('course')
      
      course = course.first()
      modules = Module.objects.filter(course=course)
      commets = Comment.objects.filter(course=course)

      ctx['course'] = course
      ctx['modules'] = modules
      ctx['comments'] = commets.order_by('date_commented')
    
      
      return render(request, template_name, ctx)