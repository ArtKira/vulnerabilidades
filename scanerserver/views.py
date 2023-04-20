from django.shortcuts import render, redirect
import nmap, json, subprocess, re
import openai
from .forms import DeviceForm

#from django.http import HttpResponse

# Create your views here.
def scan(request):#definimos las funciones a ejecutar
    return render(request, 'scan.html')

def result(request):#aqui resive la direccion IP para su escaneo
    if request.method =='POST':
        try:
            host=request.POST.get('host')
            nm=nmap.PortScanner()
            nm.scan(host,  arguments='-T5')

            statehost="Host : %s" % (host)#muestra el estado 
            state="State : %s" % nm[host].state()#estado up 
            for proto in nm[host].all_protocols():
                protocolo='Protocol : %s' % proto#indica el protocolo TCP

                lport = nm[host][proto].keys()
                sorted(lport)
            r = []
            for port in lport:#recorre todos los puertos y los muestra, muestra su estado 
                r.append('port : %s\tstate : %s' % (port, nm[host][proto][port]['state']))#se añade los resultados
            return render(request, 'result.html', {'host':statehost, 'resultado': r, 'estado':state, 'protocolo':protocolo})#retorna todos los valores
        except:
            return render(request, 'nullport.html', {'host':statehost, 'estado':state})
    return render(request, 'scan.html')
    

def whatweb(domain):
    comando = ['whatweb', '--quiet', '--log-json=-', '--color=never', domain]
    output = subprocess.check_output(comando).decode('utf-8')
    json_line = output.strip()
    resultado_json = json.loads(json_line)
    return resultado_json

def whatweb_view(request):
    if request.method == 'POST':
        domain = request.POST.get('domain')
        result = whatweb(domain)
        return render(request, 'whatweb.html', {'result': result, 'domain': domain})
    return render(request, 'whatweb.html')



def generate_text(request): # recibimos por request el puerto
    port = request.POST.get('port')
    if port:
        openai.api_key="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"#key de openAI
        prompt = f"Describe el puerto {port} y su función principal:"
        completion=openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=2048)
        answ=completion.choices[0].text
        return render(request, 'generate_text.html', {'answ': answ, 'port': port})
    else:
        return render(request, 'error.html', {'error': "El puerto proporcionado no es válido."})
    

def arp_scan_json():
    output = subprocess.check_output(["arp-scan", "--localnet"]).decode('utf-8')

    start_index = None
    for i, line in enumerate(output.splitlines()):
        if "Starting arp-scan" in line:
            start_index = i + 1
            break

    devices = []
    if start_index is not None:
        for line in output.splitlines()[start_index:]:
            match = re.match(r'(\d+\.\d+\.\d+\.\d+)\s+([\w:]+)\s+(.+)', line)
            if match:
                ip_address, mac_address, manufacturer = match.groups()
                device = {
                    'ip_address': ip_address,
                    'mac_address': mac_address,
                    'manufacturer': manufacturer
                }
                devices.append(device)
            else:
                break

    return devices

def arp_scan_view(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('arp_scan')

        devices = arp_scan_json()
        return render(request, 'arp_scan.html', {'devices': devices, 'form': form})
    else:
        devices = arp_scan_json()
        form = DeviceForm()
        return render(request, 'arp_scan.html', {'devices': devices, 'form': form})
