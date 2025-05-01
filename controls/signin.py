from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

class Signin():
      def __init__(self, request=None):
            self.request = request

      def log(self):
            ...