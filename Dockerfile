FROM archlinux

RUN apt-get update && \
    apt-get install -y whatweb nmap python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY vulnerabilidades /app/

WORKDIR /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
