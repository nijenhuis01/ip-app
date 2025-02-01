from flask import Flask, request, render_template
import requests
import socket

app = Flask(__name__)

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

    return render_template('index.html', ip_info=ip_info)

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
