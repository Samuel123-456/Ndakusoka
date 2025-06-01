from django import forms
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from student.models import Student, Enrollment, PaymentProof
from course.models import Course
from django.utils.timezone import datetime


class EnrollmentForm(forms.Form):

      def __init__(self, request=None, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.request = request


      name_certificate = forms.CharField(
            widget=forms.TextInput(
                 attrs={
                        'class': "form-control border-1 p-4 mb-2",
                        'name': 'name',
                        'id': "name",
                        'placeholder': "Nome completo para o certificado",
                        'required': "required",
                        'data-validation-required-message': "Porfavor insira seu nome para o certificado"
                  }
            )
      )

      phone_number = forms.CharField(
            max_length=9,
            min_length=9,
            widget=forms.TextInput(
                  attrs={
                        'class': "form-control border-1 p-4 mb-2",
                        'name': 'phone',
                        'id': "phone",
                        'type': "text",
                        'placeholder': "Tel (+244) ",
                        'required': "required",
                        'data-validation-required-message': "Porfavor insira seu numero de telefone"
                  }
            )
      )

      birth_date = forms.DateField(
            widget=forms.DateInput(
                  attrs={
                        'class': "form-control border-1  mb-2",
                        'name': 'birth',
                        'id': "birth",
                        'type': "date",
                        'required': "required",
                        'data-validation-required-message': "Porfavor insira seu numero de telefone"
                  }
            )
      )
 

      bio = forms.CharField(
            required=False,
            widget=forms.Textarea(
                  attrs={
                        'class': "form-control border-1  mb-2",
                        'name': 'bio',
                        'id': "bio",
                        'rows':"5",
                        'placeholder': "Porque escolheu esse curso?",
                  }
            )
      )



      def clean(self):
            cleaned_data = super().clean()

            name_certificate = cleaned_data.get('name_certificate', '').strip()
            phone_number: str = cleaned_data.get('phone_number', '').strip()

            if not name_certificate:
                  messages.add_message(self.request, messages.ERROR, 'Porfavor enforme o nome para o certificado')
                  raise forms.ValidationError('No certificate name informed')
            
            if len(name_certificate) < 5:
                  messages.add_message(self.request, messages.ERROR, 'Nome para certificado invalido')
                  raise forms.ValidationError('No certificate name informed')
            
            if not phone_number.isnumeric():
                  messages.add_message(self.request, messages.ERROR, 'Numero de telefone invalido')
                  raise forms.ValidationError('Ivalid phone number')
            
            if len(phone_number) != 9:
                  messages.add_message(self.request, messages.ERROR, 'Numero deve ter 9 digitos')
                  raise forms.ValidationError('phone number dont have 9 digits') 

            return cleaned_data 
      
      def save(self, comprovativo=None):

            #TODO: TRATAR DO PROBLEMA: UM ALUNO PODE VARIAS FAZER INSCRICOES PARA UM UNICO CURSO 

            slug_course = self.request.COOKIES.get('course')
            course = Course.objects.filter(slug=slug_course)
            if not course.exists():
                  messages.add_message(self.request, messages.ERROR, "Curso nao encontrado")
                  return redirect(f'/student/enrollment/?course={slug_course}')

            cleaned_data = super().clean()

            
            name_certificate = cleaned_data.get('name_certificate')
            phone_number = cleaned_data.get('phone_number')
            birth_date = cleaned_data.get('birth_date')
            bio = cleaned_data.get('bio')

            with transaction.atomic():
                  student = Student(
                        user=self.request.user,
                        phone=phone_number,
                        birth_date=birth_date,
                        name_certificate=name_certificate,
                        bio=bio
                  )
                  student.save()

                  enrollment = Enrollment(
                        course=course.first(),
                        student = student,
                        date_enrolled = datetime.now()
                  )

                  enrollment.save()

                  if comprovativo:
                        pp = PaymentProof(enrollment=enrollment, proof=comprovativo)
                        pp.save() 
             