from django.db import models
from Company.models import Company, Department,Role

# Create your models here.

class User(models.Model):


    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    joining_date = models.DateField(null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    role = models.ForeignKey(Role,on_delete=models.CASCADE,null=True,default='Employee')

    def __str__(self):
        return self.username



    class Meta:
        db_table = 'user_table'




class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'attendance_table'



class Leave(models.Model):
    LEAVE_STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    LEAVE_TYPE = (
        ('Sick', 'Sick Leave'),
        ('Casual', 'Casual Leave'),
        ('Paid', 'Paid Leave'),
        ('Unpaid', 'Unpaid Leave'),
    )

    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=LEAVE_STATUS, default='Pending')

    class Meta:
        db_table = 'leave_table'
