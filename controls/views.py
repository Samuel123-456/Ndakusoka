from django.shortcuts import render

# Create your views here.

def signin(request):
      template_name = 'controls/signin.html'
      ctx = {}

      return render(request, template_name, ctx)
      ...
def signup(request):
      template_name = 'controls/signup.html'
      ctx = {}

      return render(request, template_name, ctx)
      ...
def signout(request):
      ...