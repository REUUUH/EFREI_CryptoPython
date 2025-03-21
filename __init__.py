from cryptography.fernet import Fernet
from flask import Flask, jsonify
import base64

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Bienvenue sur l'API de cryptage et décryptage avec clé personnalisée !"

# Fonction pour transformer une clé utilisateur en une clé Fernet valide
def generate_fernet_key(user_key):
    """Transforme une clé utilisateur en clé Fernet valide (32 bytes en base64)"""
    user_key_bytes = user_key.encode()  # Convertir en bytes
    padded_key = user_key_bytes.ljust(32, b'\0')[:32]  # S'assurer que la clé fait 32 bytes
    return base64.urlsafe_b64encode(padded_key)  # Encoder en Base64

# Route pour chiffrer avec une clé donnée par l'utilisateur
@app.route('/encrypt/<string:key>/<string:valeur>')
def encryptage(key, valeur):
    try:
        fernet_key = generate_fernet_key(key)  # Générer une clé valide
        f = Fernet(fernet_key)  # Créer l'objet Fernet avec la clé
        valeur_bytes = valeur.encode()  # Conversion en bytes
        token = f.encrypt(valeur_bytes)  # Encryptage
        return f"Valeur encryptée : {token.decode()}"
    except Exception as e:
        return f"Erreur : {str(e)}", 400

# Route pour déchiffrer avec une clé donnée par l'utilisateur
@app.route('/decrypt/<string:key>/<string:valeur>')
def decryptage(key, valeur):
    try:
        fernet_key = generate_fernet_key(key)  # Générer une clé valide
        f = Fernet(fernet_key)  # Créer l'objet Fernet avec la clé
        valeur_decryptee = f.decrypt(valeur.encode()).decode()  # Décryptage
        return f"Valeur décryptée : {valeur_decryptee}"
    except Exception as e:
        return f"Erreur lors du décryptage : {str(e)}", 400

# Route pour générer une clé unique
@app.route('/generate_key/')
def generate_key():
    key = Fernet.generate_key().decode()  # Génération et conversion en string
    return f"Clé générée : {key}"

if __name__ == "__main__":
    app.run(debug=True)

