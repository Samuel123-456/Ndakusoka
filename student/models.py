from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.
class Student(models.Model):
      """
      Model Student
            def: Referente ao aluno a ser matriculado no site
      
      Atributos
            user (User): indica que um estudante e um e apenas um User
                  -> username, password, email, first_name, last_name, date_joined
            birth_date (date): data de nascimento do aluno

            >> Opcionais: Quando o aluno quiser aumentar dados no seu perfil <<
            phone (str): numero de telefone ou whatsapp
            profile_image (image): para a foto de perfil do aluno
            bio (str): descricao sobre o aluno
            slug (slug): indentificador na url
            token (str): chave que vai servir para alguns acessos
      Metodos
            __str__ : returna o nome de usuario do aluno
            save : cria um slug para aluno antes de salvar

      """
      user = models.OneToOneField(User, models.CASCADE)

      phone = models.CharField(max_length=9, verbose_name='tel(+244)', blank=True)
      birth_date = models.DateField(verbose_name='Data de nascimento')
      profile_image = models.ImageField(verbose_name='Foto de Perfil', upload_to='profile/', blank=True)
      bio = models.TextField(verbose_name='Descricao', blank=True)
      slug = models.SlugField(verbose_name='nome na url', default=None, blank=True)
      token = models.CharField(max_length=30, blank=True)

      #TODO: VERIFICAR SE O BLANK FUNCIONA MELHOR

      def __str__(self):
            return self.user.username
      
      def save(self, *args, **kwargs):
            if not self.slug:
                  self.slug = slugify(f'{self.user.first_name} {self.user.last_name}')
            return super().save(*args, **kwargs)
