from django.db import models
from home.models import User
from teacherLogin.models import Class
from home.models import Subject

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    year_of_study = models.IntegerField(null=True)
    semester = models.IntegerField(null=True)
    branch = models.CharField(max_length=50)
    uni_id = models.CharField(max_length=11,unique = True,null=False)
    gender = models.CharField(max_length=10)
    dob = models.DateField(null=True)

    def __str__(self):
        return self.uni_id

class EnrolledClass(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    enrolled_class_id = models.ForeignKey(Class,to_field='class_id',on_delete=models.CASCADE)
    enrolled_student_id = models.ForeignKey(Student,to_field='uni_id',on_delete=models.CASCADE)

    class Meta:
        unique_together = ('enrolled_class_id', 'enrolled_student_id',)
