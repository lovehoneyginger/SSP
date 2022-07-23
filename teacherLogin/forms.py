from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import PDF, Teacher, Class,VIDEO
from home.models import User


class TeacherSignUpForm(UserCreationForm):

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    branch = forms.CharField(required=True)
    teacher_id = forms.CharField(required=True)
    gender = forms.CharField()
    dob = forms.DateField()

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        teacher = Teacher.objects.create(user=user)
        teacher.phone_number = self.cleaned_data.get('phone_number')
        teacher.email = self.cleaned_data.get('email')
        teacher.branch = self.cleaned_data.get('branch')
        teacher.teacher_id = self.cleaned_data.get('teacher_id')
        teacher.gender = self.cleaned_data.get('gender')
        teacher.dob = self.cleaned_data.get('dob')
        teacher.save()
        return user


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ('teacher_id', 'class_id',
                  'Year_of_introduction_of_class', 'course_id')
        labels = {
            'teacher_id': 'Teacher ID',
            'class_id': 'Class ID',
            'Year_of_introduction_of_class': 'Year of introduction of class',
            'course_id': 'Course ID'
        }

    def __init__(self, *args, **kwargs):
        super(ClassForm, self).__init__(*args, **kwargs)
        self.fields['course_id'].empty_label = "Select"
        self.fields['teacher_id'].empty_label = "Select"


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class TeacherProfileUpdateForm(forms.ModelForm):
    phone_number = forms.CharField()
    email = forms.EmailField()
    branch = forms.CharField()
    gender = forms.CharField()
    dob = forms.DateField()
    class Meta:
        model = Teacher
        fields = ['phone_number', 'email', 'branch', 'gender', 'dob']


class PdfForm(forms.ModelForm):
    class Meta:
        model = PDF
        fields = ['pdf_class_id','title','pdf']


class VideoForm(forms.ModelForm):
    class Meta:
        model = VIDEO
        fields = ['video_class_id','title','video']