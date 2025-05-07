from django.db import models
from secrets import token_urlsafe

# Create your models here.
class TeacherGenerateToken(models.Model):
      """
      Model TeacherGenerateToken
            def: This model allow the admin generate a token for a teacher registration

      Atributes
            email (email): The email of the teacher to be sent the token
            token (str[30]): The token to be sent to the teacher
                  default: The default is None, for when it is  saved will generate autometically
      
      Methods:
            save: this save the data into the table and also generate the token if token is None
      """

      email = models.EmailField(verbose_name='Email do professor', unique=True)
      token = models.CharField(max_length=35, editable=None, default=None)

      def save(self, *args, **kwargs):
            if not self.token:
                  self.token = token_urlsafe(30)
            return super().save(*args, **kwargs)