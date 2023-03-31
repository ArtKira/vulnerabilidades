from django.shortcuts import render
import nmap, json, subprocess
import openai
############### Login #####################
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm

#from django.http import HttpResponse

# Create your views here.
@login_required
def scan(request):#definimos las funciones a ejecutar
    return render(request, 'scan.html')

@login_required
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
    
@login_required
def whatweb(domain):
    comando = ['whatweb', '--quiet', '--log-json=-', '--color=never', domain]
    output = subprocess.check_output(comando).decode('utf-8')
    json_line = output.strip()
    resultado_json = json.loads(json_line)
    return resultado_json

@login_required
def whatweb_view(request):
    if request.method == 'POST':
        domain = request.POST.get('domain')
        result = whatweb(domain)
        return render(request, 'whatweb.html', {'result': result, 'domain': domain})
    return render(request, 'whatweb.html')


@login_required
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


# def generate_text(request):
#     if request.method=='GET':
#         port=request.POST.get('h')
#         return render(request, 'generate_text.html', {'port':port})


############################ Login #####################################

def Login(request):
    if request.method == 'GET':
        return render(request, 'Login.html', {
            'form': CustomAuthenticationForm(),
            'title': 'Iniciar sesión en VulScaner Intelligent',
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'Login.html', {
                'form': CustomAuthenticationForm(),
                'error': 'Usuario o contraseña es incorrecta'
            })
        else:
            login(request, user)
            return redirect('scan')

'''@login_required        
def Registro(request):
    if request.method == 'GET':
        return render(request, 'Registro.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('scan')
            except:
                return render(request, 'Registro.html', {
                    'form': UserCreationForm,
                    'error': 'Usuario ya exites'
                })
        return render(request, 'Registro.html', {
            'form': UserCreationForm,
            "error": 'Contraseñas no coiciden'
        })'''

