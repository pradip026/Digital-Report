from django.shortcuts import render ,redirect
from.models import hospital
from.models import hospitalactivity
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.contrib import messages
from Doctor.models import doctor
from Patient.models import patient
from Doctor.models import doctoractivity
from Patient.models import patientactivity

def index(request):
    return render(request,'Hospital/hospitallogin.html')



def home(request):
    fullname = request.POST.get('name')
    profile=request.FILES['image']
    password = request.POST.get('passd')
    email = request.POST.get('email')
    address = request.POST.get('address')
    repassword = request.POST.get('repassd')
    number = request.POST.get('number')
    pan = request.POST.get('pan')
    try:
        validate_email(email)
        if hospital.objects.filter(hospitalemail=email).exists() or doctor.objects.filter(doctoremail=email).exists() or patient.objects.filter(patientemail=email).exists():
            messages.add_message(request, messages.INFO,'Invalid! Email or Email exists already please Enter Correctly')
            return render(request, 'Hospital/hospitallogin.html')

        elif hospital.objects.filter(hospitalpan=pan).exists():
            messages.add_message(request, messages.INFO,'Invalid! PAN number please Enter Correctly')
            return render(request, 'Hospital/hospitallogin.html')

        elif  password != repassword:
            messages.add_message(request, messages.INFO, 'Password do not match please Enter Correctly')
            return render(request, 'Hospital/hospitallogin.html')

        else:
            course_hospitaldata = hospital(hospitalname=fullname, hospitaladdress=address, hospitalemail=email, hospitalpassword=password, hospitalnumber=number, hospitalpan=pan, hospitalprofile=profile)
            course_hospitaldata.save()


            help = hospital.objects.get(hospitalemail=email)
            nam = help.hospitalname
            hid = help.id
            profile = help.hospitalprofile

            user = hospitalactivity.objects.all().order_by('?')[:10]
            user1 = doctoractivity.objects.all().order_by('?')[:10]
            user2 = patientactivity.objects.all().order_by('?')[:10]
            try:
                request.session['logged']=nam
                from django.core.mail import send_mail
                send_mail('New account Register', 'Hey there,'
                                                  '\n We have received a request that you are Register New account.'
                                                  '\n If you did not initiate this request,Inform us Immediately..'
                                                  '\n Greetings,\n Team Digital Report',
                          'nepaldigital.report@gmail.com', [email],
                          fail_silently=False)
                return render(request, 'Hospital/hospitalhome.html',{"name":nam,'id':hid,'profile':profile,'activity':user,'activity1':user1,'activity2':user2})
            except:
                return render(request, 'Hospital/hospitallogin.html')
    except ValidationError:
        messages.add_message(request, messages.INFO, 'Invalid! Email or Email exists already please Enter Correctly')

        return render(request,'Hospital/hospitallogin.html')



def loginhospital(request):
    return render(request, 'Hospital/hospitalhome.html')

def upload(request):
    try:
        if request.session.has_key('logged'):
            return render(request,'Hospital/upload.html')
        else:
            messages.add_message(request, messages.INFO,
                                 'You Are Not Logged IN.')
            return render(request, 'login.html')
    except:
        return render(request, 'login.html')


def view(request):
    try:
        if request.session.has_key('logged'):
            return render(request,'Hospital/view.html')
        else:
            messages.add_message(request, messages.INFO,
                                 'You are Not Logged IN.')
            return render(request, 'login.html')
    except:
        return render(request,'login.html')


def userdata(request):
    usertext=request.POST.get('area')

    cid=request.POST.get('submit')
    help = hospital.objects.get(id=cid)
    nam = help.hospitalname
    hid = help.id
    profile = help.hospitalprofile

    user = hospitalactivity.objects.all().order_by('?')[:10]
    user1 = doctoractivity.objects.all().order_by('?')[:10]
    user2 = patientactivity.objects.all().order_by('?')[:10]

    if usertext == "":
        name = request.POST.get('check')

        if name == 'active':
            photo = request.FILES['pic']
            h = hospitalactivity(meme=photo, postid=hid, username=nam,hospitalprofile=profile)
            h.save()
            return render(request, 'Hospital/hospitalhome.html',
                          {"name": nam, 'id': hid, 'profile': profile,'activity':user,'activity1':user1,'activity2':user2})


        return render(request, 'Hospital/hospitalhome.html',
                      {"name": nam, 'id': hid, 'profile': profile, 'activity': user,
                       'activity1': user1, 'activity2': user2})

    else:
        name = request.POST.get('check')

        if usertext !='' and name != "active":

            h = hospitalactivity(useractivity=usertext,postid=hid, username=nam,hospitalprofile=profile)
            h.save()
            return render(request, 'Hospital/hospitalhome.html',
                          {"name": nam, 'id': hid, 'profile': profile, 'activity': user, 'activity1': user1,
                           'activity2': user2})

        elif name == 'active' and usertext != '':
            print(usertext)
            photo = request.FILES['pic']
            h = hospitalactivity(useractivity=usertext, meme=photo, postid=hid, username=nam,hospitalprofile=profile)
            h.save()
            return render(request,'Hospital/hospitalhome.html',{"name":nam,'id':hid,'profile':profile,'activity':user,'activity1':user1,'activity2':user2})

        return render(request, 'Hospital/hospitalhome.html', {"name": nam, 'id': hid, 'profile': profile,'activity':user,'activity1':user1,'activity2':user2})


def out(request):
    try:
        del request.session['logged']
        return redirect('http://127.0.0.1:8000/')
    except:
        return redirect('http://127.0.0.1:8000/')