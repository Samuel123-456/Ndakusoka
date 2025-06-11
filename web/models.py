from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SocialMedia(models.Model):
      """
      Model SocialMedia
            def: Refere-se a links para redes sociais dos usuarios 

      Atributos
            user (User): O usuario desta rede social
            social_media (str): Redes Socias disponiveis
            link (url): link para a rede social do usuario
      """
      SM_CHOICES = [
            ('Wh', 'WhatsApp'),
            ('Fb', 'FaceBook'),
            ('LI', 'LinkedIn'),
      ]
      user = models.ForeignKey(User, models.CASCADE)
      social_media = models.CharField(verbose_name='Redes Sociais', choices=SM_CHOICES, max_length=100) 
      link = models.URLField(verbose_name='Link da rede social', unique=True)
