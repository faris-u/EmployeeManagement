from django.db import models

# Create your models here.


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100,null=True)
    address = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='pictures')

    def __str__(self):
        return self.name


class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=100)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)


    def __str__(self):
        return self.role

    class Meta:
        db_table= 'role'

