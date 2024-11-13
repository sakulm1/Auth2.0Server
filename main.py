from flask import Flask, request, jsonify, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key'

# Dummy-Daten
users = {'user1': 'password1'}
clients = {
    'your_client_id': {  # Gleiche ID wie im Webserver
        'client_id': 'your_client_id',
        'client_secret': 'your_client_secret',
        'redirect_uris': ['http://127.0.0.1:8000/callback'],  # Callback-URL muss genau übereinstimmen
        'default_scope': 'email',
    }
}

tokens = []


@app.route('/authorize', methods=['GET', 'POST'])
def authorize():
    # Logge die Anfrageinformationen
    client_id = request.args.get('client_id')
    redirect_uri = request.args.get('redirect_uri')

    # Überprüfe die Client-ID und die Redirect-URI
    if client_id != 'your_client_id' or redirect_uri not in clients['your_client_id']['redirect_uris']:
        print("Ungültige Client-ID oder Redirect-URI")  # Logge den Fehler
        return 'Ungültige Anfrage', 403

    if request.method == 'GET':
        return '''
            <form method="post">
                <p>Benutzername: <input type="text" name="username"></p>
                <p>Passwort: <input type="password" name="password"></p>
                <button type="submit">Autorisieren</button>
            </form>
        '''

    # Dummy-Authentifizierung
    username = request.form.get('username')
    password = request.form.get('password')
    if username in users and users[username] == password:
        auth_code = 'auth_code_example'
        print("Authentifizierung erfolgreich. Weiterleitung zu:", redirect_uri)  # Logge die Weiterleitung
        return redirect(f"{redirect_uri}?code={auth_code}", 302)

    print("Authentifizierung fehlgeschlagen")  # Logge die fehlgeschlagene Authentifizierung
    return 'Authentifizierung fehlgeschlagen', 401


@app.route('/oauth/token', methods=['POST'])
def token():
    print("Token-Anfrage erhalten:", request.form)  # Logge die Token-Anfrage
    auth_code = request.form.get('code')
    if auth_code == 'auth_code_example':
        token = {
            'access_token': 'access_token_example',
            'token_type': 'bearer',
            'expires_in': 3600
        }
        tokens.append(token['access_token'])
        print("Token erfolgreich ausgegeben:", token)  # Logge den erfolgreichen Token-Antwort
        return jsonify(token)

    print("Ungültiger Autorisierungscode")  # Logge den Fehler
    return 'Ungültiger Autorisierungscode', 400


if __name__ == '__main__':
    app.run(port=5000)

