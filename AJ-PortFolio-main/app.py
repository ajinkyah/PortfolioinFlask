from flask import Flask, render_template, request, redirect, url_for
import json
import os
import requests

app = Flask(__name__)

# Your OpenWeather API key
API_KEY = '5fa6d5d63cf82a569cf4231991c9742e'

# Route for home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for BMI Calculator page
@app.route('/bmi', methods=['GET', 'POST'])
def bmi():
    bmi = None
    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height']) / 100  # convert cm to meters
        bmi = weight / (height ** 2)
        log_bmi(weight, height * 100, bmi)
    return render_template('bmi.html', bmi=bmi)

# Function to log BMI results
def log_bmi(weight, height, bmi):
    log_entry = {
        'weight': weight,
        'height': height,
        'bmi': bmi
    }
    log_file = 'bmi_log.json'
    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            data = json.load(file)
    else:
        data = []
    data.append(log_entry)
    with open(log_file, 'w') as file:
        json.dump(data, file, indent=4)

# Route for Weather page
@app.route('/weather', methods=['GET', 'POST'])
def weather():
    weather_data = None
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather(city)
    return render_template('weather.html', weather_data=weather_data)

# Function to get weather data from OpenWeather API
def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = {
            'city': data.get('name'),
            'temperature': data.get('main', {}).get('temp'),
            'description': data.get('weather', [{}])[0].get('description'),
            'humidity': data.get('main', {}).get('humidity'),
            'wind_speed': data.get('wind', {}).get('speed')
        }
        return weather
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
