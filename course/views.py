from django.shortcuts import render, redirect, get_object_or_404
from course.models import (
      Course, 
      Module,
      Comment,
      Lesson
)
from student.models import Enrollment
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q

# Create your views here.
def viewCourses(request):
      if request.method == 'GET':
            template_name = 'course/course.html'
            ctx = {}

            ctx['courses'] = Course.objects.all()
            enrollment = Enrollment.objects.filter(Q(student__user=request.user))

            ctx['my_courses'] = [ enr.course for enr in enrollment ]
            ctx['enrollment'] = enrollment

            return render(request, template_name, ctx)

def viewCourseSingle(request, slug):
      template_name = 'course/single.html'
      ctx = {}

      course = Course.objects.filter(slug=slug)
      if not course.exists():
            return redirect('course')
      
      course = course.first()
      modules = Module.objects.filter(course=course)
      commets = Comment.objects.filter(course=course)
      student = Enrollment.objects.filter(Q(student__user=request.user) & Q(course=course))

      ctx['course'] = course
      ctx['modules'] = modules
      ctx['comments'] = commets.order_by('date_commented')
      ctx['student'] = student
      
      template_render = render(request, template_name, ctx)
      template_render.set_cookie('course', slug)
      
      return template_render

def comment(request):
      if request.method == 'POST':
            cookies = request.COOKIES
            if 'course' not in cookies:
                  return redirect('home')
            
            course = Course.objects.get(slug=cookies['course'])
            text = request.POST.get('text')

            Comment(author=request.user,course=course,text=text).save()

            return redirect(reverse('course_single', kwargs={'slug': course.slug}))

def remove_comment(request, id):
      comment = Comment.objects.filter(id=id)
      cookies = request.COOKIES
      template_name = redirect(reverse("course_single", kwargs={'slug': cookies['course']}))

      if not comment.exists():
            messages.add_message(request, messages.ERROR, 'Comentario Nao existe')
            return template_name
      comment = comment.first()

      if comment.author != request.user:
            messages.add_message(request, messages.ERROR, 'Comentario Nao pertence a esse usuario')
            return template_name
      if 'course' not in cookies:
            return redirect('home')


      comment.is_active = False
      comment.save()
      
      return template_name

def watchCourse(request, slug):
      template_name = 'course/watch.html'
      ctx = {}

      course = Course.objects.filter(slug=slug)
      if not course.exists():
            return redirect(reverse('course'))
      course = course.first()
      
      enrollement = Enrollment.objects.filter(Q(student__user=request.user) & Q(course=course))
      if not enrollement.exists():
            return redirect('course')
      
      modules = Module.objects.filter(Q(course=course))
      lessons = Lesson.objects.filter(Q(modulo__course=course))

      
      ctx['course'] = course
      ctx['modules'] = modules
      ctx['lessons'] = lessons

      ctx['is_payed'] = enrollement.first().is_payed

      #TODO: SE SLUG NAO CORRESPONDER A UMA DETERMINDA AULA, ENTAO TENHO QUE MOSTRAR A AULA INICIAL
      lesson_slug = request.GET.get('lesson')
      current_lesson = Lesson.objects.filter(slug=lesson_slug).first()
      if current_lesson:
            ctx['current_lesson'] = current_lesson

      return render(request, template_name, ctx)
