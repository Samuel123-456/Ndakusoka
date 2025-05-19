from django.shortcuts import render, redirect
from course.models import (
      Course, 
      Module,
      Comment
)
from django.contrib import messages

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
      
      template_render = render(request, template_name, ctx)
      template_render.set_cookie('course', slug)
      
      return template_render

def comment(request):
      if request.method == 'POST':
            cookies = request.COOKIES
            if 'course' not in cookies:
                  return redirect('home')
            
            course = Course.objects.get(slug=cookies['course'])
            user = request.user

            url = f'/course/course-single/{course.slug}'

            text = request.POST.get('text')

            comment = Comment(
                  author=user,
                  course=course,
                  text=text
            )

            user = comment.get_author_by_user()
            if not user:
                  messages.add_message(request, messages.ERROR, 'Somente Estudantes/Professores podem comentar')
                  return redirect(url)

            comment.save()
            return redirect(url)

def remove_comment(request, id):
      comment = Comment.objects.filter(id=id)
      cookies = request.COOKIES
      if 'course' not in cookies:
            return redirect('home')
      
      course = Course.objects.get(slug=cookies['course'])
      url = f'/course/course-single/{course.slug}'


      if not comment.exists():
            messages.add_message(request, messages.ERROR, 'Comentario Nao existe')
            return redirect(url)
      comment = comment.first()

      if comment.author != request.user:
            messages.add_message(request, messages.ERROR, 'Comentario Nao pertence a esse usuario')
            return redirect(url)


      comment.is_active = False
      comment.save()
      
      return redirect(url)
