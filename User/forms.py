from django import forms
from .models import *
from django.contrib.auth.hashers import make_password

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control w-150', 'placeholder': 'Password', 'style': 'color:brown'}),
        label='Password'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control w-150', 'placeholder': 'Confirm Password', 'style': 'color:brown'}),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'department', 'joining_date', 'salary', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control w-150', 'placeholder': 'Username', 'style': 'color:brown'}),
            'department': forms.Select(attrs={'class': 'form-select w-150', 'style': 'color:brown'}),
            'joining_date': forms.DateInput(attrs={'class': 'form-control w-150', 'type': 'date', 'style': 'color:brown'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control w-150', 'placeholder': 'Salary', 'style': 'color:brown'}),
            'role': forms.Select(attrs={'class': 'form-select w-150', 'style': 'color:brown'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = (self.cleaned_data["password"]) # Hash the password here
        if commit:
            user.save()
        return user

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username Already Taken, Please Choose Another One')
        return username


class UserUpdate(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control w-150', 'placeholder': 'Password', 'style': 'color:brown'}),
        label='Password'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control w-150', 'placeholder': 'Confirm Password', 'style': 'color:brown'}),
        label='Confirm Password'
    )
    class Meta:
        model = User
        fields = ['username', 'password', 'department', 'joining_date', 'salary', 'role']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control w-150', 'placeholder': 'Username', 'style': 'color:brown'}),
            'department': forms.Select(attrs={'class': 'form-select w-150', 'style': 'color:brown'}),
            'joining_date': forms.DateInput(
                attrs={'class': 'form-control w-150', 'type': 'date', 'style': 'color:brown'}),
            'salary': forms.NumberInput(
                attrs={'class': 'form-control w-150', 'placeholder': 'Salary', 'style': 'color:brown'}),
            'role': forms.Select(attrs={'class': 'form-select w-150', 'style': 'color:brown'}),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['check_in_time', 'check_out_time']

    def clean(self):
        cleaned_data = super().clean()
        check_in_time = cleaned_data.get("check_in_time")
        check_out_time = cleaned_data.get("check_out_time")

        if check_in_time and check_out_time and check_in_time > check_out_time:
            raise forms.ValidationError("Check-out time must be after check-in time.")

        return cleaned_data


class AddDepartment(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control w-150', 'placeholder': 'Department Name', 'style': 'color:brown'}),
        }

