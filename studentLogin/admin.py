from django.contrib import admin
from .models import Student, EnrolledClass

admin.site.register(Student)
admin.site.register(EnrolledClass)
