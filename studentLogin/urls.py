from django import urls
from django.urls import re_path, path
from . import views
urlpatterns = [
    path('register/', views.student_register.as_view(), name='student_register'),
    path('', views.login_request, name='student_login'),
    path('index/', views.index, name='student_index'),
    path('logout/', views.logout_view, name='student_logout'),
    path('index/classes/<str:class_id>', views.class_list, name='student_classes_list'),
    path('index/delete/<int:enrollment_id>/',views.class_delete, name='student_class_delete'),
    path('index/search-class/', views.search_class, name='student_search_class'),
    path('materials/', views.student_materials_index,name='student_study_material_index'),
    path('materials/<enrolled_class_id>/',views.material_select,name='student_material_type_select'),
    path('index/profile/', views.profile_update, name='student_profile_update'),
    path('pdf/<enrolled_class_id>/pdflist/',
         views.pdf_list, name='student_view_pdf'),
    path('videos/<enrolled_class_id>/videoslist/', views.video_list, name='student_view_videos'),
    re_path(r'^.*\.*', views.pages, name='student_pages'),
]
