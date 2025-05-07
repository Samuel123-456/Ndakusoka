from django.shortcuts import render, redirect
from course.models import Course, Module

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

      if not course.exists():
            return redirect('course')
      
      course = course.first()
      modules = Module.objects.filter(course=course)

      ctx['course'] = course
      ctx['modules'] = modules
      
      return render(request, template_name, ctx)