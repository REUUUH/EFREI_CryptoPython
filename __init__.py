from flask import Flask, request, render_template, redirect, url_for
import os
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

app = Flask(__name__)

def derive_key(password: str) -> bytes:
    """
    Dérive une clé de 256 bits (32 octets) à partir du mot de passe en utilisant SHA-256.
    """
    return hashlib.sha256(password.encode()).digest()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if request.method == 'POST':
        plaintext = request.form.get('plaintext')
        password = request.form.get('password')
        if not plaintext or not password:
            return render_template('encrypt_form.html', error="Veuillez renseigner tous les champs.")
        
        key = derive_key(password)
        aesgcm = AESGCM(key)
        # Génération d'un nonce aléatoire (12 octets recommandés pour AESGCM)
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
        # Le token contiendra le nonce suivi du ciphertext, encodé en base64
        token_bytes = nonce + ciphertext
        token = base64.urlsafe_b64encode(token_bytes).decode()
        
        return render_template('encrypt_result.html', token=token)
    
    return render_template('encrypt_form.html')

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    if request.method == 'POST':
        token = request.form.get('token')
        password = request.form.get('password')
        if not token or not password:
            return render_template('decrypt_form.html', error="Veuillez renseigner tous les champs.")
        
        key = derive_key(password)
        try:
            token_bytes = base64.urlsafe_b64decode(token.encode())
            # Extraction du nonce (12 octets) et du ciphertext (reste)
            nonce = token_bytes[:12]
            ciphertext = token_bytes[12:]
            aesgcm = AESGCM(key)
            plaintext = aesgcm.decrypt(nonce, ciphertext, None).decode()
            return render_template('decrypt_result.html', plaintext=plaintext)
        except Exception as e:
            return render_template('decrypt_result.html', error=f"Erreur lors du décryptage : {str(e)}")
    
    return render_template('decrypt_form.html')

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        numero = request.form.get('numero')
        
        if nom and prenom and numero:
            cursor.execute("INSERT INTO contacts (nom, prenom, numero) VALUES (?, ?, ?)", (nom, prenom, numero))
            conn.commit()
        return redirect(url_for('contacts'))
    
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()
    conn.close()
    return render_template('contacts.html', contacts=contacts)

if __name__ == '__main__':
    app.run(debug=True)
