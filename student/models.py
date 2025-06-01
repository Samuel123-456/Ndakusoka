from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from course.models import Course


# Create your models here.
class Student(models.Model):
      """
      Model Student
            def: Referente ao aluno a ser matriculado no site
      
      Attributos
            user (User): indica que um estudante e um e apenas um User
                  -> username, password, email, first_name, last_name, date_joined
            birth_date (date): data de nascimento do aluno

            >> Opcionais: Quando o aluno quiser aumentar dados no seu perfil <<
            phone (str): numero de telefone ou whatsapp
            profile_image (image): para a foto de perfil do aluno
            bio (str): descricao sobre o aluno
            slug (slug): indentificador na url
            token (str): chave que vai servir para alguns acessos
            
      Methods
            __str__ : returna o nome de usuario do aluno
            save : cria um slug para aluno antes de salvar

      """

      user = models.ForeignKey(User, models.CASCADE)

      phone = models.CharField(max_length=9, verbose_name='tel(+244)', blank=True)
      birth_date = models.DateField(verbose_name='Data de nascimento')
      name_certificate = models.CharField(max_length=100, verbose_name='Nome para o certificado')
      profile_image = models.ImageField(verbose_name='Foto de Perfil', upload_to='profile/', blank=True)
      bio = models.TextField(verbose_name='Descricao', blank=True, null=True)
      slug = models.SlugField(verbose_name='nome na url', default=None, blank=True, editable=False)
      token = models.CharField(max_length=30, blank=True, editable=False) # por equanto nao sera editavel, qual aparecer uma funcionalidade que exige

      #TODO: VERIFICAR SE O BLANK FUNCIONA MELHOR

      def __str__(self):
            return self.user.username
      
      def save(self, *args, **kwargs):
            if not self.slug:
                  self.slug = slugify(f'{self.user.first_name} {self.user.last_name}')
            return super().save(*args, **kwargs)


class Enrollment(models.Model):
      """
      Model Enrollmant
            def: Allows student to make enrollment
      
      Atributes
            course (Course): Course where Student will be enrolled to
            student (Student): Student to be enrolled
            is_payed (bool): If True, means that the course is payed else if False then the course is not payed
                  default: False
            date_enrolled (datetime): the date and time when the student is enrolled
      """

      course = models.ForeignKey(Course, models.CASCADE)
      student = models.ForeignKey(Student, models.CASCADE)
      is_payed = models.BooleanField(default=False)

      date_enrolled = models.DateTimeField(verbose_name='Data de inscricao')

      def __str__(self):
            return f'{self.student.name_certificate} ({self.course.name[:20]}...)'            
      

class PaymentProof(models.Model):
      """
      Model PaymentProof
            def: Send the reference of the payment paper to be accepted by the admin

      Attributes
            enrollment (Enrollment): the enrollment datas
            proof (File): the proof in PDF
      """
      enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
      proof = models.FileField(verbose_name='Comprovativo', upload_to='payment_proof/')

      def __str__(self):
          return self.enrollment.student.user.username
      