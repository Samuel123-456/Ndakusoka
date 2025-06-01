from django.db import models
from teacher.models import Teacher
from secrets import token_urlsafe
from random import shuffle
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
      #TODO: DOC DO COURSE
      """
      Model Course
            def: Refers to the courses that will be registered on the platform

      Attributes
            name (str): The course name
            description (str): A text, Ex: What will be taught on the platform
            teacher (Teacher): The author/Instructor of the course
            price (Decimal): The quantity in money representing the price of the course
            slug (Slug): The textcharacter that will be  shown on the url
            cover (Image): The photo of the course to be shown as the representation
            category (str): A choice of type of course that the platform offers
            created_at (date): date when the course was published

      Methods:
            __str__ : returns the course name
            save : create a slug from token_urlsafe with 16 chars and shuffles it so it can not be the same as prevention, and then makes the normal django models.save
            hour_load : returns the total of hour in the course videos

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
      
      def get_total_comments(self):
            return Comment.objects.filter(course=self, is_active=True).count()



class Module(models.Model):
      """
      Model Module
            def: Is the module of one Curso
      
      Attributes
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
      
      Attributes
            title (str): the title of the video
            time (time): the video duration (H/M/S)
            video (file): the path of the corresponding video
      Methods
            __str__ : returns the title of the video
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
      
      Attributes
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
      about = models.TextField()

      order = models.IntegerField(verbose_name='Ordem da aula', unique=True)
      date_published = models.DateTimeField(auto_now_add=True)

      slug = models.SlugField(default=None, editable=False)

      def save(self, *args, **kwargs):
            if not self.slug:
                  self.slug = token_urlsafe(8)
            return super().save(*args, **kwargs)


      def __str__(self):
            return self.title
      

class Chat(models.Model):
      """
      Model Chat
            def: Refers to the chats that my platform will have

      Attributes
            name (str): the name of the chat, not really relevante but is necessary for future plans
            slug (Slug): the representation of the chat 

      Methods
            save : creates the slug field before django default save 
      """

      CHAT_CHOICES = [
            ('Course', 'Single Course')
      ]

      name = models.CharField(max_length=20, choices=CHAT_CHOICES)
      slug = models.SlugField(default=None, editable=False)

      def save(self, *args, **kwargs):
            if not self.slug:
                  self.slug = token_urlsafe(8)
            return super().save(*args, **kwargs)
      
      def __str__(self):
            return self.name


class Comment(models.Model):
      """
      Model Comment
            def: A chat comment from users
      
      Attributes
            author (User/Teacher/Student): A user of the platform
            course (Course): The course this message belongs to
            text (str): the message to be commented
            date_commented (datetime): Refers to the date and time that this message was posted
            is_active (bool): the message will not be delated but only change the status
      """
      author = models.ForeignKey(User, models.CASCADE)
      course = models.ForeignKey(Course, models.CASCADE)
      text = models.TextField(verbose_name='Comentario')
      date_commented = models.DateTimeField(auto_now_add=True)

      is_active = models.BooleanField(default=True)

      def __str__(self):
            return self.author.username+' -> '+self.course.name
      
      def get_author_by_user(self):
            from student.models import Student
            
            my_user = [ usuario.objects.filter(user=self.author).first() for usuario in (Student, Teacher) if usuario.objects.filter(user=self.author).exists() ]
            
            return my_user[0]
