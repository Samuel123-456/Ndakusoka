from django.shortcuts import render, redirect
from controls.signup import FormSignup
from controls.signin import Control
from django.contrib.auth import login, logout

# Create your views here.

def signin(request):
      template_name = 'controls/signin.html'
      ctx = {}

      if request.method == 'POST':
            control = Control(request)
            user = control.signin()

            if user:
                  login(request, user)
                  return redirect('home')

      return render(request, template_name, ctx)

def signup(request):
      template_name = 'controls/signup.html'
      ctx = {}

      if request.method == 'GET':
            formset = FormSignup()
            ctx['formset'] = formset

            return render(request, template_name, ctx)

      if request.method == 'POST':
            formset = FormSignup(request=request, data=request.POST)

            if formset.is_valid():
                  formset.save()                  
                  return redirect('signin')
            
            ctx['formset'] = formset

            return render(request, template_name, ctx)

def signout(request):
      control = Control(request)
      is_out = control.signout()

      if not is_out:
            return redirect('')
      return redirect('signin')