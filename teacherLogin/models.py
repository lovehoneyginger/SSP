from tkinter import CASCADE
from django.db import models
from home.models import User, Subject


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    branch = models.CharField(max_length=50)
    teacher_id = models.CharField(max_length=11, unique=True, null=False)
    gender = models.CharField(max_length=10)
    dob = models.DateField(null=True)

    def __str__(self):
        return self.teacher_id


class Class(models.Model):
    teacher_id = models.ForeignKey(Teacher, to_field='teacher_id', on_delete=models.CASCADE)
    class_id = models.CharField(max_length=20, primary_key=True)
    Year_of_introduction_of_class = models.IntegerField(null=True)
    course_id = models.ForeignKey(Subject, to_field='course_id', on_delete=models.CASCADE)

    def __str__(self):
        return self.class_id


class PDF(models.Model):
    pdf_class_id = models.ForeignKey(Class, to_field='class_id', on_delete=models.CASCADE)
    title = models.CharField(max_length=100,unique=True, null=True)
    pdf = models.FileField(upload_to='pdf/',null=True,blank=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        super().delete(*args, **kwargs)


class VIDEO(models.Model):
    video_class_id = models.ForeignKey(
        Class, to_field='class_id', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True, null=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.video.delete()
        super().delete(*args, **kwargs)
