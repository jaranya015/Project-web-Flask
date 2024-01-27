# http://127.0.0.1:8000/
from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user,current_user

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/Login')
def login():
    return render_template('login.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    
    # Check for empty strings or string with only spaces
    
    if not bool(city.strip()):
        city = "Kansas City" 
    
    weather_data = get_current_weather(city)
    
    # City is not found by API
    
    if not weather_data['cod'] == 200:
        return render_template('city-not-found.html')

    title = weather_data.get("name", "Unknown City")

    return render_template(
        "weather.html",
        title=title,
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}"
    )

if __name__ == "__main__" :
    serve(app, host="0.0.0.0",port=8000)
