from django.shortcuts import render
import nmap, subprocess
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
    
def whatweb(request):#Hacemos uso del script whatweb
    if request.method == 'POST':#Verificamos que la peticion sea por post
        domain = request.POST.get('domain')# Obtenemos el nombre del dominio o direccion IP
        comando = ['whatweb', '--color=never', domain]# Establecemos el comando
        resultado = subprocess.check_output(comando).decode('utf-8')# Ejecutamos y guardamos el output del comando
        return render(request, 'whatweb.html', {'result':resultado, 'dominio':domain}) #Cargamos los datos
    return render(request, 'whatweb.html')# Entras a la plantilla vacia

def generate_text(request):#IA
    openai.api_key="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"#key de openAI
    completion=openai.Completion.create(engine="text-davinci-003", prompt="hola", max_tokens=2048)#indicamos el texto que va a crear que va a recibir 
    answ=completion.choices[0].text
    return render(request, 'generate_text.html', {'answ': answ})#caragamos los datos 

