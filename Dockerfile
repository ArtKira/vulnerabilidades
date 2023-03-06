FROM archlinux

# Actualizar y instalar curl y los paquetes necesarios.
RUN pacman -Syu --noconfirm && \
    pacman -S --noconfirm curl nmap python python-pip && \
    rm -rf /var/cache/pacman/pkg/*

# Descargar e instalar el repositorio de BlackArch.
RUN curl -O https://blackarch.org/strap.sh && \
    chmod +x strap.sh && \
    ./strap.sh

RUN pacman -S --noconfirm whatweb

# Copiar el archivo de requisitos y las vulnerabilidades de la aplicación.
COPY . /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

# Establecer el directorio de trabajo y el comando predeterminado.
WORKDIR /app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
