from django.shortcuts import render, redirect, HttpResponse,get_object_or_404

from .serializers import *

from rest_framework.response import Response
from rest_framework import status
from .forms import *
from .models import User
from django.contrib import messages
from django.contrib.sessions.models import Session
from rest_framework.decorators import api_view
import requests
from django.views.generic import TemplateView

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = User.objects.get(username=username, password=password)

        if user:
            request.session['user_id'] = user.user_id

            if user.role_id == 1:
                return redirect('/employee')
            elif user.role_id == 2:
                return redirect('/manager')
            elif user.role_id == 3:
                return redirect('/hr')


            else:
                return redirect('/')


        else:
            messages.error(request, "invalid credential,Please try again")
            return redirect('/')

    return render(request,'login.html')

def logout(request):
    from django.contrib.auth import logout as auth_logout
    auth_logout(request)
    return redirect('/')  # Redirect to the login page


def Hrpage(request):
    employees = User.objects.filter(role_id = 1)
    managers = User.objects.filter(role_id=2)
    dept = Department.objects.all()
    role = Role.objects.all()
    return render(request,"hr.html",{'managers':managers,'employees':employees,'dept':dept,'role':role})

def add_dept(request):
    if request.method == 'POST':
        form = AddDepartment(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/hr')
    else:
        form = AddDepartment()
    return render(request, 'add_dept.html', {'form': form})

def hr_profile(request):
    # Retrieve the user ID from the session
    user_id = request.session.get('user_id')

    if user_id:
        # Fetch the user from the database
        hr = get_object_or_404(User, user_id=user_id)  # Use `get_object_or_404` for better error handling
        return render(request, "hr_profile.html", {'hr': hr})
    else:
        # Handle the case where the user is not logged in
        return redirect('login')  # Redirect to login or an appropriate page

def edit_hr_profile(request):
    # Retrieve the user ID from the session
    user_id = request.session.get('user_id')

    if user_id:
        # Fetch the user from the database
        hr = get_object_or_404(User, user_id=user_id)  # Use `get_object_or_404` for better error handling
        form = UserUpdate(instance=hr)
        if request.method == 'POST':
            form = UserUpdate(request.POST, instance=hr)
            if form.is_valid():
                form.save()
                return redirect('hr_profile')
        return render(request, 'edit_hr.html', {'form': form})
    else:
        # Handle the case where the user is not logged in
        return redirect('login')  # Redirect to login or an appropriate page



def add_employee(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/hr')
    else:
        form = UserRegistrationForm()
    return render(request, 'add_employee.html', {'form': form})


def delete_employee(request,user_id):
    employee = User.objects.get(user_id=user_id)
    employee.delete()
    return redirect('/hr')

def delete_manager(request,user_id):
    manager = User.objects.get(user_id=user_id)
    manager.delete()
    return redirect('/hr')


def employee(request):
    # Access session data like a dictionary, not as a function
    user_id = request.session.get('user_id')

    if user_id:
        # Retrieve the employee (user) object by user_id
        employee = User.objects.get(user_id=user_id)  # Use 'id' as it's the default primary key field
        return render(request, "Employee.html", {'employee': employee})

    # If no user_id in session, redirect to login or handle as needed
    return redirect('/login')

def employee_profile(request):
    user_id = request.session.get('user_id')

    if user_id:
        employee = get_object_or_404(User, user_id=user_id)  # Use 'id' as it's the default primary key field
        return render(request, "employee_profile.html", {'employee': employee})

    # If no user_id in session, redirect to login or handle as needed
    return redirect('/login')
def edit_employee(request):
    user_id= request.session.get('user_id')
    if user_id:
        employee = get_object_or_404(User,user_id=user_id)
        form = UserUpdate(instance=employee)
        if request.method == 'POST':
            form = UserUpdate(request.POST, instance=employee)
            if form.is_valid():
                form.save()
                return redirect('/employee')
        return render(request, 'edit_employee.html', {'form': form})


    else:
        # Handle the case where the user is not logged in
        return redirect('login')  # Redirect to login or an appropriate page



from django.utils import timezone

def mark_attendance(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(user_id=user_id)
    today = timezone.now().date()

    if user:
        # Check if the user already has an attendance record for today
        attendance, created = Attendance.objects.get_or_create(
            employee=user,
            check_in_time__date=today,
            defaults={'check_in_time': None, 'check_out_time': None}
        )

        if request.method == 'POST':
            form = AttendanceForm(request.POST, instance=attendance)
            if form.is_valid():
                attendance = form.save(commit=False)
                if not attendance.check_in_time:
                    # Mark check-in time
                    attendance.check_in_time = timezone.now()
                elif not attendance.check_out_time:
                    # Mark check-out time
                    attendance.check_out_time = timezone.now()
                attendance.save()
                return redirect('/employee')
        else:
            form = AttendanceForm(instance=attendance)
    else:
        form = AttendanceForm()

    return render(request, 'mark_attendance.html', {'form': form})



import json
def show_attendance(request, user_id):
    # Retrieve the attendance records for the employee by user_id
    attendance_records = Attendance.objects.filter(user_id=user_id)

    # Prepare data for the chart
    attendance_data = []
    for record in attendance_records:
        if record.check_in_time and record.check_out_time:
            # Calculate the hours worked
            hours_worked = (record.check_out_time - record.check_in_time).total_seconds() / 3600
            attendance_data.append({
                'date': record.check_in_time.strftime('%Y-%m-%d'),
                'hours_worked': round(hours_worked, 2)
            })

    # Pass attendance data to the template
    return render(request, 'attendance_chart.html', {'attendance_data': json.dumps(attendance_data)})

def leave_application(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(user_id=user_id)  # Logged-in user
    if request.method == 'POST':
        # Form submission
        leave_type = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')

        if not leave_type or not start_date or not end_date or not reason:
            messages.error(request, 'All fields are required.')
        else:
            # Create a new Leave instance
            leave = Leave(
                employee=user,
                leave_type=leave_type,
                start_date=start_date,
                end_date=end_date,
                reason=reason
            )
            leave.save()

            messages.success(request, 'Leave application submitted successfully!')
            return redirect('/employee')  # Redirect to the leave application page

    # Fetch all leave records of the logged-in user
    leave_records = Leave.objects.filter(employee=user)

    return render(request, 'leave_application.html', {'leave_records': leave_records,'user':user})








def manager(request):
    user_id = request.session.get('user_id')

    if user_id:
        # Retrieve the employee (user) object by user_id
        manager = User.objects.get(user_id=user_id)
        manager_dept = manager.department
        employees =  User.objects.filter(department=manager_dept)
        return render(request, "Manager.html", {'Manager': manager,'employees':employees})

def update_manager(request):
    user_id = request.session.get('user_id')
    if user_id:
        manager = get_object_or_404(User, user_id=user_id)
        form = UserUpdate(instance=manager)
        if request.method == 'POST':
            form = UserUpdate(request.POST, instance=manager)
            if form.is_valid():
                form.save()
                return redirect('/manager')
        return render(request, 'update_manager.html', {'form': form})


    else:
        # Handle the case where the user is not logged in
        return redirect('login')  # Redirect to login or an appropriate page


def manager_delete_employee(request,user_id):
    employee = User.objects.get(user_id=user_id)
    employee.delete()
    return redirect('/manager')

















# @api_view(['GET'])
# def list_managers(request):
#     managers = User.objects.filter(role_id=2)
#     serializer = UserSerializer(managers,many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def view_manager(request,user_id):
#         manager = User.objects.get(user_id=user_id)
#         serializer = UserSerializer(manager)
#         return Response(serializer.data)
#
# @api_view(['POST'])
# def update_manager(request, user_id):
#     manager = User.objects.get(user_id=user_id)
#     serializer = UserSerializer(manager, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# @api_view(['GET'])
# def delete_manager(request,user_id):
#     manager = User.objects.get(user_id=user_id)
#     manager.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)
#
# @api_view(['GET'])
# def list_employees(request):
#     employees = User.objects.filter(role_id=1)
#     serializer = UserSerializer(employees,many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def view_employee(request,user_id):
#     employee = User.objects.get(user_id=user_id)
#     serializer = UserSerializer(employee)
#     return Response(serializer.data)
#
# @api_view(['POST'])
# def update_employee(request, user_id):
#     employee = User.objects.get(user_id=user_id)
#     serializer = UserSerializer(employee, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# @api_view(['GET'])
# def delete_employee(request, user_id):
#     employee = User.objects.get(user_id=user_id)
#     employee.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)
#
# @api_view(['GET'])
# def list_hr(request):
#     hr = User.objects.filter(role_id=3)
#     serializer = UserSerializer(hr,many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def profile(request):
#     user_id = request.session.get('user-id')
#     if user_id:
#         user = User.objects.get(user_id=user_id)
#         serializer = UserSerializer(user)
#         return render(request, 'profile.html', {'user': serializer.data})
#
#
# def profile(request):
#     api_url = "http://127.0.0.1:8000/profile"
#
#     try:
#         response = requests.get(api_url)
#         response.raise_for_status()
#
#         # Check if the response is empty or not JSON
#         if response.content:
#             data = response.json()  # Try parsing JSON
#         else:
#             data = {'error': 'Empty response'}
#     except requests.exceptions.RequestException as e:
#         data = {'error': str(e)}
#     except ValueError:
#         data = {'error': 'Invalid JSON response'}
#
#     return render(request, 'profile.html', {'data': data})
#
#
# @api_view(['POST'])
# def update_profile(request):
#     user_id = request.session.get('user_id')
#     user = User.objects.get(user_id=user_id)
#     serializer = UserSerializer(user, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
