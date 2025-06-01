from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from student.forms import EnrollmentForm
from django.urls import reverse


# Create your views here.

@login_required(login_url='signin')
def enrollment(request, slug):

      if request.method == 'GET':
            template_name = 'student/enrollment.html'
            ctx = {}

            formset = EnrollmentForm()
            ctx['formset'] = formset
            
            return render(request, template_name, ctx)

            
      
      if request.method == 'POST':
            formset = EnrollmentForm(request=request, data=request.POST)
            
            comprovativo = request.FILES.get('comprovativo', None)


            if formset.is_valid():
                  
                  formset.save(comprovativo)
                  return redirect('home')
            
            #TODO: REVERSE
            return redirect(reverse('enrollment', kwargs={'slug': request.COOKIES['course']}))

