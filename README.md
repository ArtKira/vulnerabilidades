
# VulnScan
> Vulnscan es una aplicación de escaneo de vulnerabilidades que utiliza [Editar a futuro] para proporcionar un análisis de seguridad completo de un sitio web.

<!-- ![](../header.png) -->

## Instalación

 1. Clona este repositorio en tu máquina local:

	```sh
	git clone https://github.com/ArtKira/vulnerabilidades
	```

 2. Obtén tu API key de OpenAI y añádela al archivo openai_key.txt. Si
    no tienes una API key, puedes obtenerla en la página de OpenAI.

 3. Entra en el directorio del repositorio:
 	```sh
	cd vulnerabilidades
	```

 4. Construye la imagen de Docker ejecutando el siguiente comando en la
        terminal:

	```sh
	docker build -t vulnscan/docker-django .
	```

 5. Ejecuta la imagen de Docker con el siguiente comando:

	```sh
	docker run -p 8000:8000 vulnscan/docker-django
	```
	Esto iniciará el servidor de la aplicación en el puerto 8000 de tu máquina local.

 6. Abre tu navegador web y visita la dirección http://localhost:8000 para acceder a la interfaz web de la aplicación.
 7. Ingresa la URL del sitio web que deseas escanear y presiona el botón "Scan" para iniciar el escaneo.

## Funcionalidades

 - Escaneo de puertos con Nmap
- Análisis de tecnologías web con WhatWeb
- Elaboracion de un reporte con OpenAI API
- Interfaz web fácil de usar
- Ejecución en contenedor Docker evitando problemas de compatibilidad

Agregar licecnia a futuro y crear un archivo -> ``LICENSE`` 


## Creadores

 - [https://github.com/Aguilar0607](https://github.com/Aguilar0607/)
 - [https://github.com/Aguilar0607](https://github.com/ArtKira/)
