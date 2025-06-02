# Dockerfile

# Image officielle légère Python
FROM python:3.10-slim

# Evite la génération de fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crée le dossier de travail
WORKDIR /app

# Installe les dépendances
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copie le code de l'application
COPY . /app/

# Expose le port Flask
EXPOSE 5000

# Commande pour lancer l'app
CMD ["python", "run.py"]
