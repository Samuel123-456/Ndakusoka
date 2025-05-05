from django.db import models
from teacher.models import Teacher
from secrets import token_urlsafe
from random import shuffle

# Create your models here.
class Course(models.Model):
      #TODO: DOC DO COURSE
      """
      """
      CATEGORY_CHOICES = [
            ('FC', 'FINANCAS E CONTABILIDADE'),
            ('NI', 'NEGOCIOS INTERNACIONAIS'),
            ('AG', 'ADMINISTRACAO E GESTAO'),
            ('MV', 'MARKETING E VENDAS'),
            ('EMP', 'EMPREENDEDORISMO'),
            ('AD', 'ANALISE DE DADOS'),
            ('RH', 'RECURSOS HUMANOS'),
      ]

      name = models.CharField(max_length=300)
      description = models.TextField()
      teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
      slug = models.SlugField(null=True, blank=True, default=None, unique=True, editable=False)
      price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
      cover = models.FileField(upload_to='course_cover/')
      category = models.CharField(max_length=5, choices=CATEGORY_CHOICES)
      created_at = models.DateField()

      def __str__(self):
            return self.name

      def save(self, *args, **kwargs):
            if not self.slug:
                  token = list(token_urlsafe(16))

                  shuffle(token)
                  
                  slug = ''
                  for char in token:
                        slug += char

                  self.slug = slug
            return super().save(*args, **kwargs)
      
      def hour_load(self):
            modulos = Module.objects.filter(course=self)

            total_hour = total_minute = 0
            for modulo in modulos:
                  lessons = Lesson.objects.filter(modulo=modulo)
                  hora = minuto = 0

                  for lesson in lessons:
                        hora += lesson.video.time.hour
                        minuto += lesson.video.time.minute

                  total_hour += hora
                  total_minute += minuto

            return (f'{total_hour}h {total_minute}m')



class Module(models.Model):
      """
      Model Module
            def: Is the module of one Curso
      
      Atributes
            title (str): the title of one module
            date_published (datetime): the date that this module was published
            course (Course): The course where the Module corresponde
      Methods
            __str__ : returns the title of the module
      """

      title = models.CharField(max_length=300)
      course = models.ForeignKey(Course, models.CASCADE)
      date_published = models.DateTimeField()

      def __str__(self):
            return self.title

      def total_lesson(self):
            return len(Lesson.objects.filter(modulo=self))

class Video(models.Model):
      """
      Model Video
            def: The video of one lesson
      
      Atributes
            title (str): the title of the video
            time (time): the video duration (H/M/S)
            video (file): the path of the corresponding video
      """

      title = models.CharField(max_length=300)
      time = models.TimeField(verbose_name='Duracao do video')
      video = models.FileField(verbose_name='video', upload_to='lesson_video/')

      def __str__(self):
            return self.title


class Material(models.Model):
      """
      Model Material
            def: This is the file (pdf, txt, etc) or any file the has the explanation of one video or lesson
      
      Atribute
            title (str): material titlr
            file (file): file path of the material

      Method
            __str__ : returns the material's name
      """

      title = models.CharField(max_length=200)
      file = models.FileField(verbose_name='Material de Apoio', upload_to='lesson_doc/')

      def __str__(self):
            return self.title

class Lesson(models.Model):
      """
      Model Lesson
            def: create a lesson for a module, the lesson is the relation between one video and material, the lesson can have only one video and one material
      
      Atributes
            title (str): Indicate the title of this lesson
            video (file): The video of this lesson
            materioa (file): pdf or anyother file containing the explanation od the lesson
            modulo (Module): The current lesson belongs to this Module
            order (int): Indicate the order of lesson
            date_published (datetime): the date and time that this lesson was published
      Methods
            __str__ : returns the title of this lesson
      """

      title = models.CharField(max_length=300)
      video = models.OneToOneField(Video, models.CASCADE)
      material = models.OneToOneField(Material, models.CASCADE)
      modulo = models.ForeignKey(Module, null=True, on_delete=models.CASCADE)

      order = models.IntegerField(verbose_name='Ordem da aula', unique=True)
      date_published = models.DateTimeField(auto_now_add=True)


      def __str__(self):
            return self.title


