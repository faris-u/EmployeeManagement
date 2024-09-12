"""
URL configuration for MCEMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from Company import views
from User import views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('register',views.register,name='register'),
    path('',views.login),
    path('logout',views.logout),


    path('hr',views.Hrpage),
    path('hr_profile',views.hr_profile,name='hr_profile'),
    path('edit_hr',views.edit_hr_profile,name='edit_hr'),
    path('delete_employee/<int:user_id>',views.delete_employee,name='delete_employee'),
    path('add_employee',views.add_employee,name='add_employee'),
    path('delete_manager/<int:user_id>',views.delete_manager,name='delete_manager'),
    path('employee',views.employee),
    path('employee_profile',views.employee_profile,name='employee_profile'),
    path('edit_employee',views.edit_employee,name='edit_employee'),
    path('mark_attendance',views.mark_attendance,name='mark_attendance'),
    path('attendance/<int:user_id>/', views.show_attendance, name='attendance_chat'),
    path('leave_application',views.leave_application,name='leave_application'),
    path('manager',views.manager),
    path('update_manager',views.update_manager,name='update_manager'),
    path('manager_delete_employee/<int:user_id>',views.manager_delete_employee,name='manager_delete_employee'),
    path('add_dept',views.add_dept,name='add_dept'),


    # path('company_login',views.company_login,name='company_login'),
    # path('company_register',views.company_register,name='company_register')



    # #api
    #
    #
    # path('managers',views.list_managers),
    # path('view_manager/<int:user_id>/',views.view_manager),
    # path('update_manager/<int:user_id>/',views.update_manager),
    # path('delete_manager/<int:user_id>/',views.delete_manager),
    # path('employees',views.list_employees),
    # path('view_employee/<int:user_id>/',views.view_employee),
    # path('update_employee/<int:user_id>/',views.update_employee),
    # path('delete_employee/<int:user_id>/',views.delete_employee),
    # path('hr',views.list_hr),
    # path('profile',views.profile),



]
