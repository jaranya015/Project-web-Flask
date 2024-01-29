from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # แก้ไขเป็นคีย์จริงๆ

# สร้างโมเดล User
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

# สร้างแบบฟอร์มล็อกอิน
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# กำหนด Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# กำหนดฟังก์ชันโหลดผู้ใช้
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# หน้าหลัก
@app.route('/')
def home():
    return 'หน้าหลัก - คุณ' + current_user.id if current_user.is_authenticated else 'หน้าหลัก'

# หน้าล็อกอิน
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # ตรวจสอบในระบบของคุณ (ในตัวอย่างนี้จะใช้ username: admin, password: password)
        if form.username.data == 'admin' and form.password.data == 'password':
            user = User(user_id=form.username.data)
            login_user(user)
            flash('ล็อกอินสำเร็จ!', 'success')
            return redirect(url_for('home'))
        else:
            flash('ล็อกอินไม่สำเร็จ กรุณาตรวจสอบข้อมูล', 'danger')
    return render_template('login.html', form=form)

# หน้าล็อกเอาท์
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ล็อกเอาท์สำเร็จ!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
