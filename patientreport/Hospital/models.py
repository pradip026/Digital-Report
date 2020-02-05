from django.db import models
import datetime
class hospital(models.Model):
    ID=models.AutoField
    hospitalname=models.CharField(max_length=50)
    hospitaladdress=models.CharField(max_length=50)
    hospitalemail=models.EmailField(max_length=25)
    hospitalpassword=models.CharField(max_length=10)
    hospitalnumber=models.IntegerField()
    hospitalpan=models.IntegerField()
    login_date=models.DateField(default=datetime.date.today)
    hospitalprofile=models.ImageField(upload_to="hospitalimage")


class hospitalactivity(models.Model):
    username=models.CharField(max_length=50)
    postid=models.IntegerField()
    useractivity = models.CharField(max_length=1000,default='blank')
    meme = models.ImageField(upload_to="meme", default='blank')
    uploaddate=models.DateField(default=datetime.date.today)
    hospitalprofile=models.ImageField(upload_to="hospitalimage")
