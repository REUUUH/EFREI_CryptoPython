from cryptography.fernet import Fernet, InvalidToken
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/encrypt', methods=['GET', 'POST'])
def encryptage():
    if request.method == 'POST':
        valeur = request.form['valeur']
        key = request.form['key']

        try:
            f = Fernet(key)
            valeur_bytes = valeur.encode()  # Conversion str -> bytes
            token = f.encrypt(valeur_bytes)  # Encrypt la valeur
            return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str
        except Exception as e:
            return f"Erreur lors de l'encryptage : {str(e)}", 400

    return render_template('encrypt.html')

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    if request.method == 'POST':
        encrypted_value = request.form['encrypted_value']
        key = request.form['key']

        try:
            f = Fernet(key)
            # Décrypter la valeur
            decrypted_value = f.decrypt(encrypted_value.encode())
            return f"Valeur décryptée : {decrypted_value.decode()}"
        except InvalidToken as e:
            return f"Erreur de décryptage : {str(e)}", 400
        except Exception as e:
            return f"Erreur lors du décryptage : {str(e)}", 400

    return render_template('decrypt.html')

if __name__ == "__main__":
    app.run(debug=True)
