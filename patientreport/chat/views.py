from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib import messages
import json
from Doctor.models import doctor
from Patient.models import patient
def index(request):
    try:
        if request.session.has_key('logged'):
            return render(request, 'chat/index.html', {})
        else:
            messages.add_message(request, messages.INFO,
                         'You are Not Logged IN.')
            return render(request, 'login.html')
    except:
        return render(request,'login.html')

def room(request, room_name):
    query = request.GET.get('query_name')
    try:
        if request.session.has_key('logged'):
             if doctor.objects.filter(id=query).exists() :
                user=doctor.objects.get(id=query)
                name1=user.doctorfirstname
                name2=user.doctorlastname
                profile=user.doctorprofile
                name=name1 +' '+name2
                return render(request, 'chat/room.html', {
                    'room_name_json': mark_safe(json.dumps(room_name)),'username': name,'profile':profile
                })

             elif patient.objects.filter(citizennumber=query).exists():
                user = patient.objects.get(citizennumber=query)
                name1 = user.patientfirstname
                name2 = user.patientlastname
                profile= user.patientprofile
                name = name1 + ' ' + name2
                return render(request, 'chat/room.html', {
                    'room_name_json': mark_safe(json.dumps(room_name)), 'username': name,'profile':profile
                })
             else:
                 if doctor.objects.filter(id=room_name).exists():
                     user = doctor.objects.get(id=room_name)
                     name1 = user.doctorfirstname
                     name2 = user.doctorlastname
                     profile = user.doctorprofile
                     name = name1 + ' ' + name2
                     return render(request, 'chat/room.html', {
                         'room_name_json': mark_safe(json.dumps(room_name)), 'username': name, 'profile':profile
                     })

                 elif patient.objects.filter(citizennumber=room_name).exists():
                     user = patient.objects.get(citizennumber=room_name)
                     name1 = user.patientfirstname
                     name2 = user.patientlastname
                     profile = user.patientprofile
                     name = name1 + ' ' + name2

                     return render(request, 'chat/room.html', {
                     'room_name_json': mark_safe(json.dumps(room_name)), 'username':name, 'profile':profile
                 })

        else:
            messages.add_message(request, messages.INFO,
                         'You are Not Logged IN.')
            return render(request, 'login.html')
    except:
        return render(request,'login.html')
