import os
import psycopg2
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, request

# Configuration de la DB (Lecture des variables depuis l'environnement Compose)
DB_HOST = 'db'
DB_NAME = 'appdb'
DB_USER = 'appuser'
DB_PASSWORD = 'test123!'

# Configuration du fichier de logs pour le service 'monitor'
LOG_FILE = '/app/logs/api.log'

# --- Initialisation de l'Application et Configuration du Logging ---
app = Flask(__name__)

# Configuration du logger pour écrire dans le volume partagé
# C'est la partie critique pour le service 'monitor'
file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=1024 * 1024 * 10,  # Taille max du fichier (10 MB)
    backupCount=5
)
# Format pour inclure l'heure et le niveau
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s'
))

# Ajoute le gestionnaire de fichier à l'application Flask
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

# Hook pour loguer toutes les requêtes HTTP dans le fichier
@app.after_request
def after_request(response):
    if request.path != '/' and request.path != '/api/ping-db':
        # Log le statut et le chemin de la requête pour le monitoring
        app.logger.info(f'{request.method} {request.path} {response.status_code}')
    return response
# -------------------------------------------------------------------


# Fonction de connexion à la base de données
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

# Route de validation (Ping DB)
@app.route("/api/ping-db", methods=["GET"])
def ping_db():
    try:
        conn = get_db_connection()
        conn.close()
        app.logger.info("Ping DB OK")
        return jsonify({"status": "DB Connection OK", "host_used": DB_HOST}), 200
    except Exception as e:
        app.logger.error(f"Ping DB FAILED: {str(e)}")
        return jsonify({"status": "DB Connection FAILED", "error": str(e)}), 500

# CORRIGÉ : Lecture des utilisateurs depuis la base de données
@app.route("/users", methods=["GET"])
def get_users():
    conn = None
    try:
        # Tente d'ouvrir la connexion à la DB
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Exécute la requête SQL
        cur.execute("SELECT id, name FROM users;")
        users = cur.fetchall()
        
        # Formatte le résultat en JSON
        users_list = [{"id": row[0], "name": row[1]} for row in users]
        
        cur.close()
        return jsonify(users_list), 200

    except Exception as e:
        # En cas d'erreur de connexion à la DB, retourne 500
        error_message = f"Erreur de base de données (GET /users): {e}"
        app.logger.error(error_message)
        return jsonify({"error": "Erreur de connexion à la base de données ou de lecture."}), 500

    finally:
        # Assurez-vous que la connexion est toujours fermée
        if conn:
            conn.close()

@app.route("/", methods=["GET"])
def home():
    return "API OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
