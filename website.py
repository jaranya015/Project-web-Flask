from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'azunog/icewaterorders'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# เพิ่ม Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # ระบุชื่อของหน้า login
login_manager.init_app(app)

# สร้างโมเดล User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

# ตัวอย่าง route สำหรับ login
@app.route('/login')
def login():
    user = User.query.first()
    login_user(user)
    return redirect(url_for('dashboard'))

# ตัวอย่าง route สำหรับ dashboard ที่ต้องการการเข้าสู่ระบบ
@app.route('/dashboard')
@login_required
def dashboard():
    return f'Hello, {current_user.username}!'

# ตัวอย่าง route สำหรับ logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully.'

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)