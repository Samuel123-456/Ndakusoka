from django.contrib import admin
from student.models import Student, Enrollment, PaymentProof

# Register your models here.
admin.site.register(Student)
admin.site.register(Enrollment)
admin.site.register(PaymentProof)