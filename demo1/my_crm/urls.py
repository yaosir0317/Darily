"""my_crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path
from app01 import views
urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('get_valid_img/', views.get_valid_img),
    path('logout/', views.logout, name='logout'),
    path('customer_table/', views.CustomerTableView.as_view(), name='customer_table'),
    path('customer_table_mine/', views.CustomerTableView.as_view(), name='customer_table_mine'),
    path('customer_table_all/', views.customer_table_all, name='customer_table_all'),
    path('customer_table/add/', views.AddEditCustomerTable.as_view(), name='CustomerTableAdd'),
    path('customer_statistics/', views.StatisticsView.as_view(), name="StatisticsView"),
    path('customer_statistics/charts/', views.StatisticsView.as_view(), name="StatisticsChartsView"),
    path('consult_records/add/', views.AddEditConsultRecords.as_view(), name='ConsultRecordsAdd'),
    path('consult_records/', views.ConsultRecordView.as_view(), name="ConsultRecordView"),
    path('class_study_records/', views.ClassStudyRecordView.as_view(), name="ClassStudyRecordView"),
    path('class_study_records/add/', views.AddEditClassStudyRecord.as_view(), name="ClassStudyRecordAdd"),
    path('permission/', views.permission_tree, name="PermissionView"),
    path('permission/distribute/', views.permission_distribute, name="PermissionDistributeView"),

    re_path(r'customer_table/edit/(\d+)/', views.AddEditCustomerTable.as_view(), name='CustomerTableEdit'),
    re_path(r'customer_table/delete/(\d+)/', views.CustomerTableDelete.as_view(), name='CustomerTableDelete'),
    re_path(r'consult_records/edit/(\d+)/', views.AddEditConsultRecords.as_view(), name='ConsultRecordsEdit'),
    re_path(r'consult_records/delete/(\d+)/', views.ConsultRecordsDelete.as_view(), name='ConsultRecordsDelete'),
    re_path(r'class_study_records/edit/(\d+)/', views.AddEditClassStudyRecord.as_view(), name='ClassStudyRecordEdit'),
    re_path(r'class_study_records/delete/(\d+)/', views.ClassStudyRecordDelete.as_view(), name='ClassStudyRecordDelete'),
    re_path('student_study_add/(\d+)/', views.AddStudentStudyRecord.as_view(), name="AddStudentStudyRecord"),
    re_path('^$', views.index, name='home'),
]



