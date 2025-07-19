from django.shortcuts import render, redirect
from course.models import (
      Course, 
      Module,
      Lesson
)
from student.models import Enrollment
from django.urls import reverse
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from typing import Any
from .comments import CommentView, Comment
 

# Create your views here.
      
class CourseListView(ListView):

      """CourseListView: List all courses including courses the user is included into."""

      model = Course
      template_name = 'course/course.html'
      context_object_name = 'courses'
      paginate_by = 3


      def get_context_data(self, **kwargs) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)

            if self.request.user.is_authenticated:
                  user_enrollments = Enrollment.objects.filter(Q(student__user=self.request.user))
                  context['my_courses'] = [ enrollment.course for enrollment in user_enrollments ]
            
            return context 
      

class CourseDetailView(DetailView):

      """ CourseDetailView: Show details of the course """

      model = Course
      template_name = 'course/detail.html'

      def get_context_data(self, **kwargs) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            course__slug = kwargs['object'].slug

            context["modules"] = Module.objects.filter(course__slug=course__slug)
            context["comments"] = Comment.objects.filter(course__slug=course__slug).order_by('date_commented').reverse()
            
            if self.request.user.is_authenticated:
                  context["is_student"] = Enrollment.objects.filter(Q(student__user=self.request.user) & Q(course__slug=course__slug))

            return context
      

class CommentHandler(CommentView):

      """CommentHandler: Create and Delete course comments"""

      pass


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
