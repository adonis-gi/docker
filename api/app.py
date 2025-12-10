import os
import psycopg2
from flask import Flask, jsonify

# Configuration de la DB (Lecture des variables depuis l'environnement Compose)
DB_HOST = 'db'
DB_NAME = 'appdb'
DB_USER = 'appuser'
DB_PASSWORD = 'test123!'

# Fonction de connexion à la base de données
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

app = Flask(__name__)

# Route de validation (Ping DB)
@app.route("/api/ping-db", methods=["GET"])
def ping_db():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "DB Connection OK", "host_used": DB_HOST}), 200
    except Exception as e:
        return jsonify({"status": "DB Connection FAILED", "error": str(e)}), 500

#Lecture des utilisateurs depuis la base de données
@app.route("/users", methods=["GET"])
def get_users():
    conn = None
    try:
        # Tente d'ouvrir la connexion à la DB
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Exécute la requête SQL pour récupérer les utilisateurs
        cur.execute("SELECT id, name FROM users;")
        users = cur.fetchall()
        
        # Formatte le résultat en liste de dictionnaires
        users_list = [{"id": row[0], "name": row[1]} for row in users]
        
        cur.close()
        return jsonify(users_list), 200

    except Exception as e:
        # En cas d'erreur de connexion à la DB, retourne 500
        print(f"Erreur de base de données: {e}")
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
