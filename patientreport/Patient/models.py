from django.db import models
import datetime
class patient(models.Model):
    ID=models.AutoField
    patientfirstname=models.CharField(max_length=50)
    patientlastname=models.CharField(max_length=50)
    patientaddress=models.CharField(max_length=50)
    patientemail=models.EmailField(max_length=25)
    patientpassword=models.CharField(max_length=10)
    patientnumber=models.IntegerField()
    citizennumber=models.IntegerField()
    login_date=models.DateField(default=datetime.date.today)
    patientdob=models.DateField()
    patientprofile=models.ImageField(upload_to="patientimage")
    patientpin=models.CharField(max_length=4, default="abs")






class report(models.Model):
    Citizennumber = models.IntegerField()
    Subject = models.CharField(max_length=100)
    Patientfile = models.FileField(upload_to="Report")
    Description= models.CharField(max_length=200)
    Hospitalname= models.CharField(max_length=50, default="blank")
    uploaddate = models.DateField(default=datetime.date.today)

class patientactivity(models.Model):
    username = models.CharField(max_length=50)
    postid = models.IntegerField()
    useractivity = models.CharField(max_length=1000, default='blank')
    meme = models.ImageField(upload_to="meme", default='blank')
    uploaddate = models.DateField(default=datetime.date.today)
    patientprofile=models.ImageField(upload_to="patientimage")
