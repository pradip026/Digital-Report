from django.shortcuts import render
from.models import doctor
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.contrib import messages
from.models import doctoractivity
from Hospital.models import hospital
from Patient.models import patient
from Hospital.models import hospitalactivity
from Patient.models import patientactivity

def index(request):
    return render(request,'Doctor/doctorlogin.html')

def home(request):
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    profile = request.FILES['image']
    password = request.POST.get('password')
    email = request.POST.get('email')
    address = request.POST.get('address')
    repassword = request.POST.get('repassword')
    number = request.POST.get('number')
    pan = request.POST.get('pan')
    try:
        validate_email(email)
        if doctor.objects.filter(doctoremail=email).exists() or hospital.objects.filter(hospitalemail=email).exists() or patient.objects.filter(patientemail=email).exists():
            messages.add_message(request, messages.INFO,
                                 'Invalid! Email or Email exists already please Enter Correctly')
            return render(request, 'Doctor/doctorlogin.html')

        elif doctor.objects.filter(doctorliscence=pan).exists():
            messages.add_message(request, messages.INFO, 'Invalid! PAN number please Enter Correctly')
            return render(request, 'Doctor/doctorlogin.html')

        elif password != repassword:
            messages.add_message(request, messages.INFO, 'Password do not match please Enter Correctly')
            return render(request, 'Doctor/doctorlogin.html')

        else:
            course_doctordata = doctor(doctorfirstname=firstname, doctorlastname=lastname, doctoraddress=address, doctoremail=email,
                                           doctorpassword=password, doctornumber=number, doctorliscence=pan,
                                           doctorprofile=profile)
            course_doctordata.save()

            help = doctor.objects.get(doctoremail=email)
            nam1 = help.doctorfirstname
            nam2 = help.doctorlastname
            nam=nam1+' '+nam2
            hid = help.id
            profile = help.doctorprofile

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
                return render(request, 'Doctor/doctorhome.html',{"name": nam, 'id': hid, 'profile': profile, 'activity': user,'activity1':user1,'activity2':user2})
            except:
                return render(request, 'Doctor/doctorlogin.html')
    except ValidationError:
        messages.add_message(request, messages.INFO, 'Invalid! Email or Email exists already please Enter Correctly')
        return render(request,'Doctor/doctorhome.html')



def userdata(request):
    usertext = request.POST.get('area')
    cid = request.POST.get('submit')
    help = doctor.objects.get(id=cid)
    nam1 = help.doctorfirstname
    nam2 = help.doctorlastname
    nam = nam1 + ' ' + nam2
    hid = help.id
    profile = help.doctorprofile
    user = hospitalactivity.objects.all().order_by('?')[:10]
    user1 = doctoractivity.objects.all().order_by('?')[:10]
    user2 = patientactivity.objects.all().order_by('?')[:10]

    if usertext == "":
        name = request.POST.get('check')
        if name == 'active':
            photo = request.FILES['pic']
            h = doctoractivity(meme=photo, postid=hid, username=nam, doctorprofile=profile)
            h.save()
            return render(request, 'Doctor/doctorhome.html',
                          {"name": nam, 'id': hid, 'profile': profile, 'activity': user,'activity1':user1,'activity2':user2})


        return render(request, 'Doctor/doctorhome.html',
                      {"name": nam,'id': hid, 'profile': profile, 'activity': user,'activity1':user1,'activity2':user2})



    else:
        name = request.POST.get('check')
        if usertext !='' and name != "active":
            h = doctoractivity(useractivity=usertext, postid=hid, username=nam, doctorprofile=profile)
            h.save()
            return render(request, 'Doctor/doctorhome.html',
                          {"name": nam, 'id': hid, 'profile': profile, 'activity': user, 'activity1': user1,
                           'activity2': user2})

        elif name == 'active' and usertext != '':
            photo = request.FILES['pic']
            h = doctoractivity(useractivity=usertext, meme=photo, postid=hid, username=nam, doctorprofile=profile)
            h.save()
            return render(request, 'Doctor/doctorhome.html',
                          {"name": nam,'id': hid, 'profile': profile, 'activity': user,'activity1':user1,'activity2':user2})
        return render(request, 'Doctor/doctorhome.html',
                      {"name": nam, 'id': hid, 'profile': profile, 'activity': user,'activity1':user1,'activity2':user2})
