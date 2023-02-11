from django.shortcuts import render
import nmap

#from django.http import HttpResponse

# Create your views here.
def scan(request):#definimos las funciones a ejecutar
    return render(request, 'scan.html')

def result(request):#aqui resive la direccion IP para su escaneo
    host=request.GET.get('host')
    nm=nmap.PortScanner()
    nm.scan(host, arguments='-T5')

    statehost="Host : %s" % (host)#muestra el estado 
    state="State : %s" % nm[host].state()#estado up 
    for proto in nm[host].all_protocols():
        protocolo='Protocol : %s' % proto#indica el protocolo TCP

        lport = nm[host][proto].keys()
        sorted(lport)
    r = []
    for port in lport:#recorre todos los puertos y los muestra, muestra su estado 
        r.append('port : %s\tstate : %s' % (port, nm[host][proto][port]['state']))
    return render(request, 'result.html', {'host':statehost, 'resultado': r, 'estado':state, 'protocolo':protocolo})#retorna todos los valores