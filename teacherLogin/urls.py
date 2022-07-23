from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('register/', views.teacher_register.as_view(), name='teacher_register'),
    path('', views.login_request, name='teacher_login'),
    path('index/', views.index, name='teacher_index'),
    path('logout/', views.logout_view, name='teacher_logout'),
    path('index/classes/', views.class_list, name='teacher_classes_list'),
    path('index/add-class/', views.add_class, name='teacher_add_class'),
    path('index/delete/<class_id>/', views.class_delete, name='teacher_class_delete'),
    path('pdf/<class_id>',views.pdf_creation,name='class_pdf_creation'),
    path('pdf/<class_id>/pdflist/',views.pdf_list, name = 'view_pdf'),
    path('pdf/<class_id>/pdflist/upload/', views.teacher_pdf_upload, name='teacher_pdf_upload'),
    path('pdf/delete/<pk>/', views.teacher_pdf_delete, name='teacher_delete_pdf'),
    path('videos/<class_id>/videoslist/', views.video_list, name='view_videos'),
    path('videos/<class_id>/videoslist/upload/', views.teacher_video_upload, name='teacher_video_upload'),
    path('videos/delete/<pk>/', views.teacher_video_delete, name='teacher_delete_video'),
    path('materials/', views.materials_index,name='teacher_study_material_index'),
    path('materials/<class_id>/',views.material_select,name='teacher_material_type_select'),
    path('class/<class_id>', views.teacher_student_list, name='teacher_student_list'),
    path('index/profile/', views.profile_update, name='teacher_profile_update'),
    re_path(r'^.*\.*', views.pages, name='teacher_pages'),
]
