from flask import Flask, request, render_template
import requests
import socket
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuratie voor Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Gmail SMTP server
app.config['MAIL_PORT'] = 587  # De poort voor TLS
app.config['MAIL_USE_TLS'] = True  # Zorg ervoor dat je TLS gebruikt
app.config['MAIL_USE_SSL'] = False  # Geen SSL nodig voor Gmail met poort 587
app.config['MAIL_USERNAME'] = 'ipzoeker@gmail.com'  # Je Gmail-emailadres
app.config['MAIL_PASSWORD'] = 'mngx oyym bwaz pprc'  # Je Gmail-wachtwoord (of app-wachtwoord)
app.config['MAIL_DEFAULT_SENDER'] = 'ipzoeker@gmail.com'  # Standaard afzender

# Initialiseren van Flask-Mail
mail = Mail(app)

def get_ip_info(ip_or_url):
    """Haalt geolocatiegegevens op van een IP-adres of URL via ipinfo.io"""
    try:
        # Controleer of het een domeinnaam is en converteer naar een IP
        if not ip_or_url.replace('.', '').isdigit():
            ip_or_url = socket.gethostbyname(ip_or_url)

        # Haal IP-info op van ipinfo.io
        response = requests.get(f'https://ipinfo.io/{ip_or_url}/json')
        data = response.json()

        return {
            "ip": ip_or_url,
            "locatie": data.get("city", "Onbekend") + ", " + data.get("country", "Onbekend"),
            "provider": data.get("org", "Onbekend"),
        }
    except Exception as e:
        print(f"Fout bij ophalen van IP-info: {e}")
        return {"ip": ip_or_url, "locatie": "Onbekend", "provider": "Onbekend"}

@app.route('/', methods=['GET', 'POST'])
def home():
    ip_info = None
    if request.method == 'POST':
        user_input = request.form.get('ip_or_url')
        if user_input:
            ip_info = get_ip_info(user_input)
        # Verzend een test-e-mail als een POST-verzoek wordt gedaan
        if 'email' in request.form:
            send_email()

    return render_template('index.html', ip_info=ip_info)

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if name and email and message:
            send_email(name, email, message)
            return render_template('contact.html', message_sent=True)

    return render_template('contact.html', message_sent=False)


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

def send_email(name, email, message):
    """Functie om een e-mail te verzenden via Gmail"""
    try:
        msg = Message("Nieuw bericht via Contactformulier",
                      recipients=["jouw_email@gmail.com"])  # Ontvanger van de e-mail
        msg.body = f"Naam: {name}\nEmail: {email}\nBericht:\n{message}"
        mail.send(msg)
        print("E-mail verzonden!")
    except Exception as e:
        print(f"Fout bij verzenden van e-mail: {e}")


if __name__ == '__main__':
    app.run(debug=True)
