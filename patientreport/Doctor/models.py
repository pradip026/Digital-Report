from django.db import models
import datetime
class doctor(models.Model):
    ID=models.AutoField
    doctorfirstname=models.CharField(max_length=50)
    doctorlastname=models.CharField(max_length=50)
    doctoraddress=models.CharField(max_length=50)
    doctoremail=models.EmailField(max_length=25)
    doctorpassword=models.CharField(max_length=10)
    doctornumber=models.IntegerField()
    doctorliscence=models.IntegerField()
    login_date=models.DateField(default=datetime.date.today)
    doctorprofile=models.ImageField(upload_to="doctorimage")


class doctoractivity(models.Model):
    username=models.CharField(max_length=50)
    postid=models.IntegerField()
    useractivity = models.CharField(max_length=1000,default='blank')
    meme = models.ImageField(upload_to="meme", default='blank')
    uploaddate=models.DateField(default=datetime.date.today)
    doctorprofile=models.ImageField(upload_to="doctorimage")
