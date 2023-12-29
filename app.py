from sqlalchemy.orm.exc import NoResultFound
from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from datetime import datetime
import secrets
from models import db, User, Car

current_year = datetime.now().year

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://thimmy:Uydnv1$1@localhost/thimmy_car?charset=utf8mb4'
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)




login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



@app.context_processor
def custom_context():
    return {
        'company': 'Bthimmy',
        'year': current_year,
    }

@app.route("/")
def home():
    cars = Car.query.limit(10).all()
    print(cars)
    return render_template('homepage.html', cars=cars)





@app.route('/details/<car_id>')
def details(car_id):
    try:
        car = Car.query.filter_by(id=car_id).first()
        if not car:
            raise NoResultFound
    except NoResultFound:
        return redirect(url_for('home'))

    print("Hello")
    print(car)
    print("Hello")
    return render_template("detail.html", car=car)





@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username.title()).first()

        if user is None:
            return render_template('login.html', message='User Does Not Exist')

        elif not user.check_password(password):
            return render_template('login.html', message='Password is wrong')

        else:
            login_user(user)
            # next = request.args.get('next')
            return redirect(url_for('admin'))

            



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))




@app.route("/register", methods = ['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username'].title()
        password = request.form['password']
        mail = request.form['mail'].lower()
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        existing_user = User.query.filter_by(username = username).first()
        existing_mail = User.query.filter_by(email = mail).first()

        if password != confirm_password:
            return render_template('register.html', message = 'Password Does Not Match')
        
        if existing_user:
            return render_template('register.html', message = 'Username already in use')
        
        elif existing_mail:
            return render_template('register.html', message = 'Mail Already in use')
        
        new_user = User(username=username, email=mail)
        new_user.set_password(password)
        print(len(new_user.password_hash))
        print("Done")
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('admin'))
        





@app.route("/admin")
@login_required
def admin():
    return render_template('admin.html', cars = Car.query.all())


if __name__ == '__main__':
    app.run(debug=True)
