from django.http import HttpResponse
from django.template import RequestContext, loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django import forms
import serial
from time import sleep
import subprocess 

def index(request):
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    write_string = ''
    run = 1
    write = bytes('\n','utf-8')
    ser.write(write)
    while run == 1:
        line = bytes(ser.readline())  
        if line.startswith(b'login:'):
            write_string = 'root\n'
        elif line.startswith(b'root@%'):
            write_string = 'cli\n'
        elif line.startswith(b'root>'):
            write_string = 'configure\n'
        elif line.startswith(b'root#'):
            write_string = 'set system root-authentication encrypted-password "$1$msJTsUFh$eliIRD8Xs07ktw18Qw/Nm/"\n'
            write = bytes(write_string,'utf-8')
            ser.write(write)
            write_string = 'set system host-name deploy\n'
            write = bytes(write_string,'utf-8')
            ser.write(write)
            write_string = 'set system login user deploy class super-user\n'
            write = bytes(write_string,'utf-8')
            ser.write(write)
            write_string = 'set system login user deploy authentication encrypted-password "$1$9T7EKhkn$BMDd9i8E8nuVSFDkiLfU5/"\n'
            run = 0
        else:
            write_string = ''
        write = bytes(write_string,'utf-8')
        ser.write(write)
        
    write = bytes('commit\n','utf-8')
    ser.write(write)
    return HttpResponse(line)

def upgrade(request):
    subprocess.check_output(["jlogin", "-l", "/dev/null"])
    

def firebox(request, poll_id):
    if request.method == 'POST':
        p = get_object_or_404(Poll, pk=poll_id)
        config = p.choice_set.get(pk=request.POST['config'])
            ###### do stuff

            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
        return render(request, 'results.html', {'poll': p})
    else:
        return render(request, 'firebox_form.html' )

