from flask import Flask, request, jsonify
import requests
from requests.exceptions import RequestException

app = Flask(__name__)


def get_real_time_temperature(city):
    api_key = '74030c6f3c85639c932e43da1def2925'
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': api_key, 'units': 'metric'} 
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        return temperature
    else:
        return None
    
def get_location_info(ip):
    response = requests.get(f"http://ip-api.com/json/{ip}")
    response.raise_for_status()
    data = response.json()
    return {
        "city": data.get("city", "Unknown")
    }

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Guest')
    client_ip = request.remote_addr


    try:
        location_info = get_location_info(client_ip)
        city = location_info['city']
        temperature = get_real_time_temperature(city)

        if temperature is not None:
            greeting = f"Hello, {visitor_name}!, The temperature is {temperature} degrees Celsius in {city}"

            response = {
                "client_ip": client_ip,
                "location": city,
                "greeting": greeting
            }
            return jsonify(response)
        else:
            return jsonify({"error": "Unable to fetch real-time temperature information"}), 500
    except RequestException as e:
        return jsonify({"error": "Unable to fetch location information"}), 500



if __name__ == '__main__':
    app.run()
   