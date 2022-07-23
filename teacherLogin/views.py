from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView
from home.models import User,Subject
from .forms import TeacherSignUpForm, ClassForm, UserUpdateForm, TeacherProfileUpdateForm,PdfForm,VideoForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.template import loader
from .models import Teacher, Class,PDF,VIDEO
from studentLogin.models import EnrolledClass, Student

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


class teacher_register(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = '../templates/teacher_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/teacher/')


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_student == False and user.is_teacher == True:
                login(request, user)
                return redirect('teacher_index')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, '../templates/login.html',
                  context={'form': AuthenticationForm()})


def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('teach_dash/index.html')
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

        html_template = loader.get_template('teach_dash/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('teach_dash/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('teach_dash/page-500.html')
        return HttpResponse(html_template.render(context, request))


def class_list(request):
    current_user = request.user
    q1 = Teacher.objects.get(user=current_user.id)
    q2 = Class.objects.filter(teacher_id=q1.teacher_id)
    context = {'class_list': q2}
    return render(request, "../templates/teach_dash/classlist.html", context)


def class_delete(request, class_id):
    c = Class.objects.get(pk=class_id)
    c.delete()
    return redirect('teacher_classes_list')


def add_class(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = ClassForm()
        else:
            c = Class.objects.get(pk=id)
            form = ClassForm(instance=c)
        return render(request, "../templates/teach_dash/addclass.html", {'form': form})
    else:
        if id == 0:
            form = ClassForm(request.POST)
        else:
            c = Class.objects.get(pk=id)
            form = ClassForm(request.POST, instance=c)
        if form.is_valid():
            form.save()
        return redirect('teacher_classes_list')


def pdf_creation(request,class_id):
    buf = io.BytesIO()
    c = canvas.Canvas(buf,pagesize=letter,bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",14)

    lines =[]
    current_user = request.user
    u = User.objects.get(pk=current_user.id)

    c1 = Class.objects.get(class_id = class_id)
    lines.append('                                   SSP CLASS LIST')
    lines.append('                                 AISAT,KALAMASSERY')
    lines.append(str(c1.class_id))
    lines.append(str(c1.Year_of_introduction_of_class))
    name  = str(u.first_name)+" "+str(u.last_name)
    lines.append(str(name))
    lines.append(str(c1.teacher_id))
    lines.append(str(c1.course_id))

    d = Subject.objects.get(course_id=c1.course_id)
    lines.append(str(d.course_name))

    lines.append(' ')
    lines.append(' ')
    e = EnrolledClass.objects.filter(enrolled_class_id = c1)
    lines.append('University ID      Semester         Branch')
    for ec in e:
        f = Student.objects.get(uni_id = ec.enrolled_student_id)
        lines.append('------------------------------------------------------')
        lines.append(str(f.uni_id)+"                     " + str(f.semester)+"                   "+str(f.branch))
    
    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename = 'class.pdf')

def materials_index(request):
    current_user = request.user
    q1 = Teacher.objects.get(user=current_user.id)
    q2 = Class.objects.filter(teacher_id=q1.teacher_id)
    context = {'class_list': q2}
    return render(request, "../templates/teach_dash/materialsindex.html", context)


def teacher_student_list(request,class_id):
    c1 = Class.objects.get(class_id=class_id)
    e = EnrolledClass.objects.filter(enrolled_class_id=c1)
    list =[]
    for ec in e:
        f = Student.objects.get(uni_id=ec.enrolled_student_id)
        list.append(f)
    print(list[0].semester)
    context = {'student_list': list}
    return render(request, "../templates/teach_dash/studentlist.html",context)


def profile_update(request):
    if request.method == 'POST':
        current_user = request.user
        q1 = Teacher.objects.get(user=current_user.id)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        t_form = TeacherProfileUpdateForm(request.POST,
                                   instance=q1)
        if u_form.is_valid() and t_form.is_valid():
            u_form.save()
            t_form.save()
            messages.success(request)
            return redirect('teacher_profile_update')

    else:
        current_user = request.user
        q1 = Teacher.objects.get(user=current_user.id)
        u_form = UserUpdateForm(instance=request.user)
        t_form = TeacherProfileUpdateForm(instance=q1)

    context = {
        'u_form': u_form,
        't_form': t_form
    }
    return render(request, 'teach_dash/profile.html', context)


def material_select(request,class_id):
    context={'class_id':class_id}
    return render(request, 'teach_dash/materialselect.html',context)


def pdf_list(request,class_id):
    q1 = PDF.objects.filter(pdf_class_id=class_id)
    if not q1:
        c = {
            'class_id':class_id
        }
        return render(request,'teach_dash/emptypdflist.html',c)
    context = {'pdf':q1,'class_id':class_id}
    html_template = loader.get_template('teach_dash/pdflist.html')
    return HttpResponse(html_template.render(context, request))


def teacher_pdf_upload(request,class_id):
    if request.method == 'POST':
        form = PdfForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_pdf',class_id)
    else:
        form = PdfForm()
    return render(request, 'teach_dash/uploadpdf.html', {
        'form': form,
        'class_id': class_id
    })


def teacher_pdf_delete(request, pk):
    if request.method == 'POST':
        pdf = PDF.objects.get(pk=pk)
        class_id = pdf.pdf_class_id
        pdf.delete()
    return redirect('view_pdf',class_id)


def video_list(request, class_id):
    q1 = VIDEO.objects.filter(video_class_id=class_id)
    if not q1:
        c = {
            'class_id': class_id
        }
        return render(request, 'teach_dash/emptyvideolist.html', c)
    context = {'video': q1, 'class_id': class_id}
    html_template = loader.get_template('teach_dash/videolist.html')
    return HttpResponse(html_template.render(context, request))


def teacher_video_upload(request, class_id):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_videos', class_id)
    else:
        form = VideoForm()
    return render(request, 'teach_dash/uploadvideo.html', {
        'form': form,
        'class_id': class_id
    })


def teacher_video_delete(request, pk):
    if request.method == 'POST':
        video = VIDEO.objects.get(pk=pk)
        class_id = video.video_class_id
        video.delete()
    return redirect('view_videos', class_id)
