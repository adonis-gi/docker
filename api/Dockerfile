# Image de base
FROM python:3.11-slim

# Dossier de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY . .

# L'API écoute sur le port 8000
EXPOSE 8000

# Commande de démarrage
CMD ["python", "app.py"]

#Lancement de apt update
RUN apt update

#Création user non-root
RUN useradd -m appuser

#Créer dossier logs et donner les droits de lecture seulement
RUN mkdir -p /app/logs && chown -R appuser:appuser /app


USER appuser

ENV PORT=8000
EXPOSE 8000
