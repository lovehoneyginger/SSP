from django import template
from django.urls import reverse
from django.views.generic import CreateView
from home.models import User, Subject
from .forms import StudentSignUpForm,UserUpdateForm,StudentProfileUpdateForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import Student, EnrolledClass
from teacherLogin.models import Class,Teacher,PDF,VIDEO
from django.db.models import Q

class student_register(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = '../templates/student_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/student/')


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_student == True and user.is_teacher == False:
                login(request, user)
                return redirect('student_index')
            else:
                messages.error(request, "Invalid university id or password")
        else:
            messages.error(request, "Invalid university id or password")
    return render(request, '../templates/stud_login.html',
                  context={'form': AuthenticationForm()})


def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('stud_dash/index.html')
    return HttpResponse(html_template.render(context, request))


def logout_view(request):
    logout(request)
    return redirect('/')


def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('stud_dash/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('stud_dash/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('stud_dash/page-500.html')
        return HttpResponse(html_template.render(context, request))


def class_list(request,class_id):
    current_user = request.user
    c1 = Student.objects.get(user=current_user.id)
    try:
        t1 = Class.objects.get(class_id=class_id)
    except:
        t1 = Class.objects.all()
    print(t1)
    if request.method == 'POST':
        if t1:
            EnrolledClass.objects.create(enrolled_class_id=t1,enrolled_student_id=c1)
    current_user = request.user
    q1 = Student.objects.get(user=current_user.id)
    q2 = EnrolledClass.objects.filter(enrolled_student_id=q1.uni_id)
    context = {'class_list': q2}
    return render(request, "../templates/stud_dash/classlist.html", context)


def class_delete(request, enrollment_id):
    c = EnrolledClass.objects.get(pk=enrollment_id)
    c.delete()
    return redirect('student_classes_list','nothing')


def search_class(request):
    data = Class.objects.filter(class_id='nul')
    if 'q' in request.POST:
        q = request.POST['q']
        # data = Data.objects.filter(last_name__icontains=q)
        multiple_q = Q(class_id__contains=q)
        print(multiple_q)
        data = Class.objects.filter(multiple_q)
        print(data)
    else:
        return render(request, 'stud_dash/searchclass.html')
    context = {
        'dat': data
    }
    return render(request, 'stud_dash/classadd.html', context)

def student_materials_index(request):
    current_user = request.user
    q1 = Student.objects.get(user=current_user.id)
    q2 = EnrolledClass.objects.filter(enrolled_student_id=q1.uni_id)
    context = {'class_list': q2}
    return render(request, "../templates/stud_dash/materialsindex.html", context)



def material_select(request, enrolled_class_id):
    context = {'enrolled_class_id': enrolled_class_id}
    return render(request, 'stud_dash/materialselect.html', context)


def profile_update(request):
    if request.method == 'POST':
        current_user = request.user
        q1 = Student.objects.get(user=current_user.id)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        s_form = StudentProfileUpdateForm(request.POST,
                                          instance=q1)
        if u_form.is_valid() and s_form.is_valid():
            u_form.save()
            s_form.save()
            messages.success(request)
            return redirect('student_profile_update')

    else:
        current_user = request.user
        q1 = Student.objects.get(user=current_user.id)
        u_form = UserUpdateForm(instance=request.user)
        s_form = StudentProfileUpdateForm(instance=q1)

    context = {
        'u_form': u_form,
        's_form': s_form
    }
    return render(request, 'stud_dash/profile.html', context)


def pdf_list(request, enrolled_class_id):
    q1 = PDF.objects.filter(pdf_class_id=enrolled_class_id)
    if not q1:
        c = {
            'enrolled_class_id': enrolled_class_id
        }
        return render(request, 'stud_dash/emptypdflist.html', c)
    context = {'pdf': q1, 'enrolled_class_id': enrolled_class_id}
    html_template = loader.get_template('stud_dash/pdflist.html')
    return HttpResponse(html_template.render(context, request))


def video_list(request, enrolled_class_id):
    q1 = VIDEO.objects.filter(video_class_id=enrolled_class_id)
    if not q1:
        c = {
            'enrolled_class_id': enrolled_class_id
        }
        return render(request, 'stud_dash/emptyvideolist.html', c)
    context = {'video': q1, 'enrolled_class_id': enrolled_class_id}
    html_template = loader.get_template('stud_dash/videolist.html')
    return HttpResponse(html_template.render(context, request))
