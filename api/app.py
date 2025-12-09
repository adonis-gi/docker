import os
import psycopg2
from flask import Flask, jsonify

# Configuration de la DB
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

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify([
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ])

@app.route("/", methods=["GET"])
def home():
    return "API OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
