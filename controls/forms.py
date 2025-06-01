from django import forms
from django.contrib import messages
import secrets
from student.models import Student
from django.contrib.auth.models import User
from django.db import transaction

class FormSignup(forms.Form):


      def __init__(self, request=None, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.request = request


      first_name = forms.CharField(
            widget=forms.TextInput(
                  attrs={
                        'class': "form-control border-1 p-4 mr-2",
                        'name': 'fname',
                        'id': "fname",
                        'placeholder': "primeiro nome",
                        'required': "required",
                        'data-validation-required-message': "Porfavor insira seu primeiro nome"
                  }
            )
      )

      last_name = forms.CharField(
            widget=forms.TextInput(
                  attrs={
                        'class': "form-control border-1 p-4 mb-2",
                        'name': 'lname',
                        'id': "lname",
                        'placeholder': "ultimo nome",
                        'required': "required",
                        'data-validation-required-message': "Porfavor insira seu ultimo nome"
                  }
            )
      )

      email = forms.EmailField(
            widget=forms.EmailInput(
                  attrs={
                        'class': "form-control border-1 p-4 mb-2",
                        'name': 'email',
                        'id': "email",
                        'placeholder': "email",
                        'required': "required",
                        'data-validation-required-message': "Porfavor insira seu email"
                  }
            )
      )

      password = forms.CharField(
            widget=forms.PasswordInput(
                  attrs={
                        'class': "form-control border-1 p-4 mr-2",
                        'name': 'password',
                        'id': "password",
                        'type': "password",
                        'placeholder': "senha",
                        'required': "required",
                        'data-validation-required-message': "Porfavor insira sua senha"
                  }
            )
      )

      confirm_password = forms.CharField(
            widget=forms.PasswordInput(
                  attrs={
                        'class': "form-control border-1 p-4",
                        'name': 'password',
                        'id': "password",
                        'type': "password",
                        'placeholder': "confirma senha",
                        'required': "required",
                        'data-validation-required-message': "Porfavor insira sua senha"
                  }
            )
      )



      def clean(self):
            cleaned = super().clean()

            first_name: str = cleaned.get('first_name', '').strip()
            last_name: str = cleaned.get('last_name', '').strip()
            email: str = cleaned.get('email', '').strip()
            password: str = cleaned.get('password', '').strip()
            confirm_password: str = cleaned.get('confirm_password', '').strip()

            if not first_name.isalpha():
                  messages.add_message(self.request, messages.WARNING, 'Nome contem numero/especiais/vazio')
                  raise forms.ValidationError('numeric/especial character found')
            
            if not last_name.isalpha():
                  messages.add_message(self.request, messages.WARNING, 'Sobre contem numero/especiais/vazio')
                  raise forms.ValidationError('numeric/especial character found')

            if not email:
                  messages.add_message(self.request, messages.WARNING, 'Email nao foi informado')
                  raise forms.ValidationError('Email not informed')
            
            if User.objects.filter(email=email).exists():
                  messages.add_message(self.request, messages.ERROR, 'Este email ja existe')
                  raise forms.ValidationError('User email already exists')
            
            if User.objects.filter(username=first_name+last_name).exists():
                  messages.add_message(self.request, messages.ERROR, 'Usuario com este nome ja existe')
                  raise forms.ValidationError('Username already exists')

            
            if not password:
                  messages.add_message(self.request, messages.WARNING, 'senha nao foi informado')
                  raise forms.ValidationError('Password not informed')
            
            if len(password) < 5:
                  messages.add_message(self.request, messages.WARNING, 'senha menor que 5 caracteres')
                  raise forms.ValidationError('Weak password')

            if not secrets.compare_digest(password, confirm_password):
                  messages.add_message(self.request, messages.WARNING, 'Senhas diferentes')
                  raise forms.ValidationError('Wrong password Confirmation')


            return cleaned
      
      def save(self):
            data_cleaned = super().clean()

            
            first_name: str = data_cleaned.get('first_name')
            last_name: str = data_cleaned.get('last_name')
            email: str = data_cleaned.get('email')
            password: str = data_cleaned.get('password')



            with transaction.atomic():
                  User.objects.create_user(
                        username=first_name+last_name,
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name
                  )

                  messages.add_message(self.request, messages.SUCCESS, 'Usuario cadastrado com sucesso')