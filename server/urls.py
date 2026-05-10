"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from web import views
from web.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('about/', views.about, name = 'about'),
    path('contact/', views.contact, name = 'contact'),
    path('courses/', SubjectListView.as_view(), name = 'courses'),
    path('team/', views.team, name = 'team'),
    path('testimonial/', views.testimonial, name = 'testimonial'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('afterlogin', views.afterlogin,name='afterlogin'),
    path('quiz_list/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.start_quiz, name='start_quiz'),
    path('subjects/', SubjectListView.as_view(), name='subject_list'),  # Danh sách môn học
    path('subjects/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),  # Chi tiết bài học
    path('summary_report/', views.summary_report, name = 'summary_report'),
    path('admin_blank/', views.admin_blank, name='admin_blank'),
    path('buttons/', views.buttons, name = 'buttons'),
    path('typography/', views.typography, name = 'typography'),
    path('other_element/', views.other_element, name = 'other_element'),
    path('widgets/', views.widgets, name = 'widgets'),
    path('forms/', views.forms, name = 'forms'),
    path('tables/', views.tables, name = 'tables'),
    path('charts/', views.charts, name = 'charts'),

    path('students/add/', views.add_student, name='add_student'),
    path('students/edit/<int:id>/', views.edit_student, name='edit_student'),
    path('students/delete/<int:id>/', views.delete_student, name='delete_student'),
    path('students/', views.student_list, name='student_list'),

    path('subjects_list/', views.subjects_list, name='subjects_list'),
    path('subjects/add/', views.subject_add, name='subject_add'),
    path('subjects/edit/<int:id>/', views.subject_edit, name='subject_edit'),
    path('subjects/delete/<int:id>/', views.subject_delete, name='subject_delete'),

    path('lessons/', LessonListView.as_view(), name='lesson_list'),  # Xem tất cả bài học
    path('lessons/add/', LessonAddView.as_view(), name='lesson_add'),  # Thêm bài học
    path('lessons/edit/<int:id>/', LessonEditView.as_view(), name='lesson_edit'),  # Sửa bài học
    path('lessons/delete/<int:id>/', LessonDeleteView.as_view(), name='lesson_delete'),  # Xóa bài học

    path('documents/', views.documentation_list, name='documentation_list'),
    path('documents/add/', views.documentation_add, name='documentation_add'),
    path('documents/edit/<int:pk>/', views.documentation_edit, name='documentation_edit'),
    path('documents/delete/<int:pk>/', documentation_delete, name='documentation_delete'),

    path('quizzes/', views.quiz_overviews, name='quiz_overviews'),
    path('quizzes/add/', views.quiz_add, name='quiz_add'),
    path('quizzes/edit/<int:pk>/', views.quiz_edit, name='quiz_edit'),
    path('quizzes/delete/<int:pk>/', views.quiz_delete, name='quiz_delete'),

    path('questions/', views.question_list, name='question_list'),
    path('questions/add/', views.add_question, name='add_question'),  # Đảm bảo rằng dòng này có mặt
    path('questions/edit/<int:pk>/', views.edit_question, name='edit_question'),
    path('questions/delete/<int:pk>/', views.delete_question, name='delete_question'),

    path('test_student/', views.test_student, name='test_student'),
    path('gender-distribution/', gender_distribution, name='gender_distribution'),

    path('new_dashboard', views.new_dashboard, name='new_dashboard'),
    path('new_add_student', views.new_add_student, name='new_add_student'),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
