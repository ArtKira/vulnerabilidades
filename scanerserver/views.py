from django.shortcuts import render
import nmap, json, subprocess
import openai

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
    port = request.GET.get('port')
    if port:
        openai.api_key=""#key de openAI
        prompt = f"Describe el puerto {port} y su función principal:"
        completion=openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=2048)
        answ=completion.choices[0].text
        return render(request, 'generate_text.html', {'answ': answ, 'port': port})
    else:
        return render(request, 'error.html', {'error': "El puerto proporcionado no es válido."})


# def generate_text(request):
#     if request.method=='GET':
#         port=request.POST.get('h')
#         return render(request, 'generate_text.html', {'port':port})