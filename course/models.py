from django.db import models

# Create your models here.
class Module(models.Model):
      """
      Model Module
            def: Is the module of one Curso
      
      Atributes
            title (str): the title of one module
            date_published (datetime): the date that this module was published

      Methods
            __str__ : returns the title of the module
      """

      title = models.CharField(max_length=300)
      date_published = models.DateTimeField()

      def __str__(self):
            return self.title


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


