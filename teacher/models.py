from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from secrets import token_urlsafe

# Create your models here.
class Teacher(models.Model):
      """
      Model Teacher
            def: Referente ao professor/instrutor de um curso
      
      Atributos
            user (User): indica que um estudante e um e apenas um User
                  -> username, password, email, first_name, last_name, date_joined

            profile_image (image): para a foto de perfil do instrutor
            bio (str): descricao sobre o instrutor
            slug (slug): indentificador na url
            token (str): chave que vai servir para alguns acessos
      Metodos
            __str__ : returna o nome de usuario do instrutor
            save : cria um slug para instrutor antes de salvar

      """
      FIELD_CHOICES = [
            ('TA', 'TECNICO EM ADMINISTRACAO'),
            ('TC', 'TECNICO EM COMERCIO'),
            ('TCE', 'TECNICO EM COMERCIO EXTERIOR'),
            ('TCB', 'TECNICO EM CONTABILIDADE'),
            ('TF', 'TECNICO EM FINANCAS'),
            ('TM', 'TECNICO EM MARKETING'),
            ('TL', 'TECNICO EM LOGISTICA'),
            ('TRH', 'TECNICO EM RECURSOS HUMANOS'),
      ]

      user = models.ForeignKey(User, models.CASCADE)

      profile_image = models.ImageField(verbose_name='foto de perfil', upload_to='profile/')
      bio = models.TextField(verbose_name='Discricao')
      field = models.CharField(max_length=5, choices=FIELD_CHOICES)
      slug = models.SlugField(verbose_name='nome na url', default=None, editable=False)
      token = models.CharField(max_length=30, blank=True, unique=True, editable=False)

      def __str__(self):
            return f'{self.user.first_name} {self.user.last_name}'

      def save(self, *args, **kwargs):
            if not self.slug:
                  self.slug = slugify(f'{self.user.first_name} {self.user.last_name}')
            
            if not self.token:
                  self.token = token_urlsafe()
            
            return super().save(*args, **kwargs)
      
