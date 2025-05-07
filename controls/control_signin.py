from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib import messages

class Control():
      def __init__(self, request=None):
            self.request = request
            self.email = self.request.POST.get('email')
            self.password = self.request.POST.get('password')

      def signin(self):
            username = self._get_username()
            user = authenticate(self.request, username=username, password=self.password)

            if not user:
                  messages.add_message(self.request, messages.ERROR, 'Usuario nao encontrado, confira as credenciais')
                  return None
            
            return user

      def _get_username(self):
            user = User.objects.filter(email=self.email)
            return user.first().username if user.exists() else None
      
      def signout(self):
            if self.request.user.is_authenticated:
                  logout(self.request)
                  
                  messages.add_message(self.request, messages.SUCCESS, 'Logout feito com sucesso')
                  return True
            messages.add_message(self.request, messages.ERROR, 'usuario nao esta logado')
            return False