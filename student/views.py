from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from student.forms import EnrollmentForm


# Create your views here.

@login_required(login_url='signin')
def enrollment(request):
      template_name = 'student/enrollment.html'
      ctx = {}

      if request.method == 'GET':

            formset = EnrollmentForm()
            ctx['formset'] = formset

            template_render = render(request, template_name, ctx)
            course_slug = request.GET.get('course', None)

            if course_slug:
                  template_render.set_cookie('course', course_slug)
            
            return template_render

            
      
      if request.method == 'POST':
            formset = EnrollmentForm(request=request, data=request.POST)

            if formset.is_valid():
                  return redirect('home')
            
            cookies = request.COOKIES.get('course')
            return redirect(f'/student/enrollment/?course={cookies}')

