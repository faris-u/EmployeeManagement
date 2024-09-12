# from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
# from .models import *
# from User.models import *
# from.forms import *
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
#
#
#
#
# def company_register(request):
#     if request.method == 'POST':
#         form = CompanyRegistrationForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Company registered successfully!")
#             return redirect('login')  # Redirect after successful registration
#     else:
#         form = CompanyRegistrationForm()
#
#     return render(request, 'register_company.html', {'form': form})
#
# def company_login(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         password = request.POST.get('password')
#
#
#         company = Company.objects.get(name=name, password=password)
#         if company:
#             request.session['company_id'] = company.company_id
#         else:
#             messages.error(request, "invalid credential,Please try again")
#             return redirect('/')
#
# # Create your views here.
# def company_view(request):
#     # Retrieve company_id from the session
#     company_id = request.session.get('company_id')
#
#     # Handle case where company_id is not present in the session
#     if company_id is None:
#         return HttpResponse('Company ID not found in session.')
#
#     # Get the company by ID, or return a 404 error if not found
#     company = get_object_or_404(Company, id=company_id)
#
#     # Get all departments in the company
#     departments_in_company = Department.objects.filter(company=company)
#
#     # Get all users who belong to those departments
#     users = User.objects.filter(department__in=departments_in_company)
#
#     # Render the template with company and users context
#     return render(request, 'Company.html', {'company': company, 'users': users})
# #
# #
