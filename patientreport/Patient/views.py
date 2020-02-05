from django.shortcuts import render
from.models import patient
from.models import report
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import HttpResponse,Http404,FileResponse
from django.contrib import messages
from wsgiref.util import FileWrapper
from.models import patientactivity
from Doctor.models import doctor
from Hospital.models import hospital
from Doctor.models import doctoractivity
from Hospital.models import hospitalactivity
def index(request):
    return render(request,'Patient/patientlogin.html')

def home(request):
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    profile = request.FILES['image']
    password = request.POST.get('password')
    pin = request.POST.get('pin')
    email = request.POST.get('email')
    address = request.POST.get('address')
    patientdob = request.POST.get('dob')
    repassword = request.POST.get('repassword')
    number = request.POST.get('number')
    citizennumber = request.POST.get('cnumber')
    try:
        validate_email(email)
        if patient.objects.filter(patientemail=email).exists() or hospital.objects.filter(hospitalemail=email).exists() or  doctor.objects.filter(doctoremail=email).exists():
            messages.add_message(request, messages.INFO,
                                 'Invalid! Email or Email exists already please Enter Correctly !')
            return render(request, 'Patient/patientlogin.html')

        elif patient.objects.filter(citizennumber=citizennumber).exists():
            messages.add_message(request, messages.INFO, 'Invalid! Citizenship number please Enter Correctly !')
            return render(request, 'Patient/patientlogin.html')

        elif password != repassword:
            messages.add_message(request, messages.INFO, 'Password donot match please Enter Correctly !')
            return render(request, 'Patient/patientlogin.html')

        else:
            patientdata = patient(patientfirstname=firstname, patientlastname=lastname, patientaddress=address,
                                       patientemail=email,
                                       patientpassword=password, patientnumber=number, citizennumber=citizennumber,patientdob=patientdob,
                                       patientprofile=profile, patientpin=pin)
            patientdata.save()

            help = patient.objects.get(patientemail=email)
            nam1= help.patientfirstname
            nam2 = help.patientlastname
            num=help.citizennumber
            nam=nam1+' '+nam2
            hid = help.id
            profile = help.patientprofile

            user = hospitalactivity.objects.all().order_by('?')[:10]
            user1 = doctoractivity.objects.all().order_by('?')[:10]
            user2 = patientactivity.objects.all().order_by('?')[:10]
            try:
                request.session['logged']=nam
                from django.core.mail import send_mail
                send_mail('New account Register', 'Hey there,'
                                                  '\n We have received a request that you are Register New account.'
                                                  '\n If you did not initiate this request,Inform us Immediately.'
                                                  '\n Greetings,\n Team Digital Report',
                          'nepaldigital.report@gmail.com', [email],
                          fail_silently=False)
                return render(request, 'Patient/patienthome.html',{"name": nam, 'id': hid,'number':num, 'profile': profile, 'activity': user,'activity1':user1,'activity2':user2})
            except:
                return render(request, 'Patient/patientlogin.html')
    except ValidationError:
        messages.add_message(request, messages.INFO, 'Invalid! Email or Email exists already please Enter Correctly !')
        return render(request, 'home.html')



def upload(request):
    try:
        if request.session.has_key('logged'):
            global numb
            numb=request.POST.get('number')
            if patient.objects.filter(citizennumber=numb):
                citizen=patient.objects.get(citizennumber=numb)
                return render(request,'Patient/upload.html',{'citizens':citizen})

            else:
                messages.add_message(request, messages.INFO, 'Citizenship number you have entered is not found or patient account is not created ! ')
                return render(request, 'Hospital/upload.html')
        else:
            messages.add_message(request, messages.INFO,
                                 'You Are Not Logged IN.')
            return render(request, 'login.html')

    except:
        return render(request, 'login.html')


def post(request):
    global numb
    numbers=request.POST.get('number')
    hospitalname=request.POST.get('hospital')
    subject=request.POST.get('subject')
    file=request.FILES['file']
    description=request.POST.get('message')
    if report.objects.filter(Citizennumber=numbers).exists() and report.objects.filter(Subject=subject).exists():
        citizen = patient.objects.get(citizennumber=numb)
        messages.add_message(request, messages.INFO,
                             'Report with same Subject with same citizenship number already Exists !')
        return render(request, 'Patient/upload.html', {'citizens': citizen})

    elif numb==numbers:
        reportdata=report(Citizennumber=numb,Subject=subject,Patientfile=file,Description=description,Hospitalname=hospitalname)
        reportdata.save()

        usermail=patient.objects.get(citizennumber=numb)
        email = usermail.patientemail
        from django.core.mail import send_mail
        send_mail('New File Detected on your Account', 'Hey there,'
                                                '\n We have received a new file on your Account.\nPosted by:'+ hospitalname +
                                                                                   '\n If you did not Authorized it let us to know.'
                                                                                   '\n Greetings,\n Team Digital Report',
                  'nepaldigital.report@gmail.com', [email],
                  fail_silently=False)

        return render(request,'success.html')

    else:
        citizen = patient.objects.get(citizennumber=numb)
        messages.add_message(request, messages.INFO,
                             'Entered citizenship number does not match ! ')
        return render(request, 'Patient/upload.html', {'citizens': citizen})


def view(request):
    try:
        if request.session.has_key('logged'):
            citizen1=request.POST.get('number')
            pin=request.POST.get('passd')
            if report.objects.filter(Citizennumber=citizen1).exists():
                setpin=patient.objects.get(citizennumber=citizen1)
                data=setpin.patientpin
                if pin==data:
                    value=report.objects.all().order_by('-uploaddate')
                    return render(request,'Patient/view.html',{'values':value,'cit':int(citizen1)})

                else:
                    messages.add_message(request, messages.INFO,
                                         'Incorrect Pin Enter again ! ')
                    return render(request, 'Hospital/view.html')

            else:
                messages.add_message(request, messages.INFO,
                                     'Incorrect Details or File does not Exists try again ! ')
                return render(request, 'Hospital/view.html')
        else:
            messages.add_message(request, messages.INFO,
                                 '     You Are Not Logged IN.')
            return render(request, 'login.html')
    except:
        return render(request,'login.html')







def show(request):
    block=report.objects.all()
    for ob in block:
        a=str(ob.id)
        path=str(ob.Patientfile)
        filename=path
        if a in request.POST:
            try:
                if filename.endswith('.pdf'):
                    return FileResponse(open('media/' + path, 'rb'), content_type='application/pdf')

                else:
                     return HttpResponse(open('media/'+path, 'rb'), content_type="image/png")

            except FileNotFoundError:
                raise Http404()




def down(request):
    block=report.objects.all()
    for ob in block:
        a=str(ob.id)
        path=str(ob.Patientfile)
        if a in request.POST:
            filename = 'media/'+path
            wrapper = FileWrapper(open(filename, 'rb'))
            response = HttpResponse(wrapper, content_type="application/pdf")
            response['Content-Disposition'] = "attachment; filename=" + filename
            return response




def userdata(request):
    usertext = request.POST.get('area')
    cid = request.POST.get('submit')
    help = patient.objects.get(id=cid)
    nam1 = help.patientfirstname
    nam2 = help.patientlastname
    nam=nam1+' '+nam2
    hid = help.citizennumber
    profile = help.patientprofile

    user = hospitalactivity.objects.all().order_by('?')[:10]
    user1 = doctoractivity.objects.all().order_by('?')[:10]
    user2 = patientactivity.objects.all().order_by('?')[:10]

    if usertext == '':
        name = request.POST.get('check')
        if name == 'active':

            photo = request.FILES['pic']
            h = patientactivity(meme=photo, postid=hid, username=nam, patientprofile=profile)
            h.save()
            return render(request, 'Patient/patienthome.html',
                          {"name": nam, 'number': hid, 'profile': profile, 'activity': user,'activity1':user1,'activity2':user2})


        return render(request, 'Patient/patienthome.html',
                      {"name": nam,'number': hid, 'profile': profile, 'activity':user,'activity1':user1,'activity2':user2})



    else:
        name = request.POST.get('check')
        if usertext != '' and name != 'active':
            h = patientactivity(useractivity=usertext, postid=hid, username=nam, patientprofile=profile)
            h.save()
            return render(request, 'Patient/patienthome.html',
                          {"name": nam, 'number': hid, 'profile': profile, 'activity': user, 'activity1': user1,
                           'activity2': user2})

        elif name == 'active' and usertext != '':
            photo = request.FILES['pic']
            h = patientactivity(useractivity=usertext, meme=photo, postid=hid, username=nam, patientprofile=profile)
            h.save()
            return render(request, 'Patient/patienthome.html',
                          {"name": nam,'number': hid, 'profile': profile, 'activity': user,'activity1':user1,'activity2':user2})
        return render(request, 'Patient/patienthome.html',
                      {"name": nam, 'number': hid, 'profile': profile, 'activity': user,'activity1':user1,'activity2':user2})
