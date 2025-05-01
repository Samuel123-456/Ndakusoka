from django.shortcuts import render

# Create your views here.
def home(request):
      template_name = 'web/index.html'
      ctx = {}

      return render(request, template_name, ctx)

      # TODO: DISPONIBILIZAR APENAS 3 CURSOS NO HOME PAGE


def teachers(request):
      template_name = 'web/teacher.html'
      ctx = {}

      return render(request, template_name, ctx)

      # TODO: USAR JS PARA QUANDO CLICAR NUM MENU ELE PINTA O RECENTE 