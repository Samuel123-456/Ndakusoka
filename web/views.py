from django.shortcuts import render
from teacher.models import Teacher
from django.core.paginator import Paginator
from django.views.generic import TemplateView

# Create your views here.
class HomeTemplateView(TemplateView):
      template_name = 'web/index.html'

      # TODO: DISPONIBILIZAR APENAS 3 CURSOS NO HOME PAGE


def teachers(request):
      template_name = 'web/teacher.html'
      ctx = {}

      currunt_page = int(request.GET.get('page', 1))
      
      paginator = Paginator(list(Teacher.objects.all()), 4)
      paginator = paginator.get_page(currunt_page)
      
      ctx['paginator'] = paginator
      
      return render(request, template_name, ctx)

      # TODO: USAR JS PARA QUANDO CLICAR NUM MENU ELE PINTA O RECENTE 


class AboutTemplateView(TemplateView):
      template_name = 'web/about.html'


def contact(request):
      template_name = 'web/contact.html'
      ctx = {}

      return render(request, template_name, ctx)