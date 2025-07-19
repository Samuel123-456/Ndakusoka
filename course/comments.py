from django.shortcuts import redirect
from course.models import (
      Course, 
      Comment,
)
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
 

class CommentView:
      
      @classmethod
      def create_comment(self, request, slug: str):
            url = reverse("course:detail-course", kwargs={"slug": slug})

            course = Course.objects.filter(slug=slug)
            if course.exists() == False: return redirect(url)
            
            text_comment = str(request.POST.get('text', None)).strip()
            if not text_comment: return redirect(url)
            

            Comment.objects.create(author=request.user, course=course.first(), text=text_comment)
            return redirect(url)
      
      
      @classmethod
      def delete_comment(self, request, id: str, slug: str):
            comment = Comment.objects.filter(Q(author=request.user) & Q(id=id))
            if comment.exists():
                  comment.first().delete()
            else:
                  messages.add_message(request, messages.ERROR, "Comentario nao foi removido")
            
            return redirect(reverse("course:detail-course", kwargs={"slug": slug}))
     
