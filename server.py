# http://127.0.0.1:8000/
from flask import Flask, render_template, request, redirect, url_for, flash
from weather import get_current_weather
from waitress import serve
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user,current_user

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

    flash_messages = list(get_flashed_messages())
    return render_template('login.html', flashed_messages=flash_messages)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

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
    with app.app_context():
        db.create_all()

    serve(app, host="0.0.0.0",port=8000)
