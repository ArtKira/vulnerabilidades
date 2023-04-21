from django.shortcuts import render, redirect
import nmap, json, subprocess, re
import openai
from .forms import DeviceForm
from .models import Device
from django.http import FileResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
#from django.http import HttpResponse

# Create your views here.
def scan(request):#definimos las funciones a ejecutar
    return render(request, 'scan.html')

def scan(request):
    devices = Device.objects.all() # Recupera todos los dispositivos guardados en la base de datos
    return render(request, 'scan.html', {'devices': devices})

def result(request):#aqui recibe la direccion IP para su escaneo
    if request.method =='POST':
        host=request.POST.get('host')
        statehost="Host : %s" % (host)#muestra el estado 
        
        if not host:
            return render(request, 'error.html', {'error': "Por favor, ingresa una dirección IP válida."})
        
        try:
            nm=nmap.PortScanner()
            nm.scan(host,  arguments='-T5')
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



def generate_text(request):
    port = request.POST.get('port')
    if port:
        openai.api_key = "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"
        prompt = f"Elabora un reporte como si fueras un experto sobre el puerto {port} y función principal y las posibles vulnerabilidades que tiene:"
        completion = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=4000)
        answ = completion.choices[0].text

        if request.GET.get('download', None) == 'pdf':
            buffer = create_pdf(port, answ)
            response = FileResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename=Reporte_Puerto_{port}.pdf'
            return response
        else:
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

def create_pdf(port, text):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    pdf.setTitle(f"Reporte Puerto {port}")

    pdf.setStrokeColor(colors.black)
    pdf.setLineWidth(2)
    pdf.rect(20, 20, letter[0] - 40, letter[1] - 40)

    # Encabezado
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(300, 750, f"Puerto: {port}")

    # Texto del cuerpo
    pdf.setFont("Helvetica", 12)
    text_lines = text.splitlines()
    y = 720
    max_width = 500  # Establece el ancho máximo del texto en el PDF
    margin_left = 50

    for line in text_lines:
        words = line.split()
        x = margin_left
        for word in words:
            if x + pdf.stringWidth(word) > max_width:
                y -= 14
                x = margin_left
            pdf.drawString(x, y, word)
            x += pdf.stringWidth(word + " ")
        y -= 14

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer