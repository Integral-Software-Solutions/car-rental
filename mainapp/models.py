from django.db import models

# Create your models here.
class Enquiry(models.Model):
    name=models.CharField(max_length=50)
    emailaddress=models.EmailField(max_length=100)
    subject=models.CharField(max_length=500)
    message=models.CharField(max_length=5000)

class Customer(models.Model):
    name=models.CharField(max_length=50)
    contactno=models.CharField(max_length=10,primary_key=True)
    emailaddress=models.EmailField(max_length=100)
    dob=models.CharField(max_length=30)
    gender=models.CharField(max_length=6)
    address=models.CharField(max_length=1000)
    city=models.CharField(max_length=500)
    state=models.CharField(max_length=500)
    zipcode=models.CharField(max_length=6)

class Login(models.Model):
    userid=models.CharField(max_length=100, primary_key=True)
    password=models.CharField(max_length=30)
    usertype=models.CharField(max_length=30)

class Feedback(models.Model):
    fid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    contactno = models.CharField(max_length=10)
    emailaddress = models.EmailField(max_length=100)
    feedback = models.CharField(max_length=5000)
    feedbackdate = models.CharField(max_length=30)

class Complaint(models.Model):
    cid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    contactno = models.CharField(max_length=10)
    emailaddress = models.EmailField(max_length=100)
    complaint = models.CharField(max_length=5000)
    complaintdate = models.CharField(max_length=30)
    status = models.CharField(max_length=20, default='pending')
