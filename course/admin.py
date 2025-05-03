from django.contrib import admin
from course.models import (
      Video,
      Lesson,
      Material,
      Module
)

# Register your models here.
admin.site.register(Video)
admin.site.register(Lesson)
admin.site.register(Material)
admin.site.register(Module)