# http://127.0.0.1:8000/
from flask import send_file
from flask_migrate import Migrate
from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from weather import get_current_weather
from heart import beat
import turtle
from models import db, User
from waitress import serve
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__, static_folder='assets/static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
login_manager = LoginManager(app)
login_manager.login_view = 'login' 
login_manager.init_app(app)

db.init_app(app)
migrate = Migrate(app, db) 

@app.route('/download')
def download():
    beat()
    return render_template('download.html')

@app.route('/download_file')
def download_file():
    # Logic การดาวน์โหลดไฟล์ เช่น ดึงไฟล์จากแหล่งเก็บข้อมูล
    return send_file('path/to/file', as_attachment=True)


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
    return render_template('login.html') 

@app.route('/blog')
def blog():
    return render_template("blog.html")

@login_required
@app.route('/weather')
def get_weather():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    city = request.args.get('city')
    
    # Check for empty strings or string with only spaces
    
    if not bool(city.strip()):
        city = "Thailand" 
    
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')

        # Ensure username is not empty
        if not username:
            flash('Username is required', 'error')
            return redirect(url_for('register'))

        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            return 'Username already exists'

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, name=name, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html')

if __name__ == "__main__" :
    serve(app, host="0.0.0.0",port=8000)
