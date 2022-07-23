from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import Student,EnrolledClass
from home.models import User


class StudentSignUpForm(UserCreationForm):

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    year_of_study = forms.IntegerField(required=True)
    semester = forms.IntegerField(required=True)
    branch = forms.CharField(required=True)
    uni_id = forms.CharField(required=True)
    gender = forms.CharField()
    dob = forms.DateField()

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        student = Student.objects.create(user=user)
        student.phone_number = self.cleaned_data.get('phone_number')
        student.email = self.cleaned_data.get('email')
        student.year_of_study = self.cleaned_data.get('year_of_study')
        student.semester = self.cleaned_data.get('semester')
        student.branch = self.cleaned_data.get('branch')
        student.uni_id = self.cleaned_data.get('uni_id')
        student.gender = self.cleaned_data.get('gender')
        student.dob = self.cleaned_data.get('dob')
        student.save()
        return user


class EnrolledClassForm(forms.ModelForm):
    class Meta:
        model = EnrolledClass
        fields = ( 'enrolled_class_id','enrolled_student_id')
        labels = {
            'enrolled_class_id': 'enrolled_class_id',
            'enrolled_student_id': 'enrolled_student_id',
        }


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class StudentProfileUpdateForm(forms.ModelForm):
    phone_number = forms.CharField()
    email = forms.EmailField()
    year_of_study = forms.CharField
    semester = forms.CharField()
    branch = forms.CharField()
    gender = forms.CharField()
    dob = forms.DateField()

    class Meta:
        model = Student
        fields = ['phone_number', 'email',
                  'year_of_study', 'semester', 'branch', 'gender', 'dob']
